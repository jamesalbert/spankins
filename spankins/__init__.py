#!/usr/bin/env python

"""spankins

Usage:
  spankins auth --url=<url> --username=<username> (--password=<password>|--token=<token>) [--profile=<profile>]
  spankins ping --profile=<profile>
  spankins send <file> --profile=<profile> [--out=<out>]
  spankins send template <file> --profile=<profile> (--arg=<key>=<val>)... [--out=<out>]
  spankins diagnose --profile=<profile> [--out=<out>]
  spankins master add <name> --profile=<profile> [--out=<out>]
  spankins agent-port set <port> --profile=<profile> [--out=<out>]
  spankins (-h | --help)
  spankins --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt

import requests, os
from pathlib import Path
from jinja2 import Template
from json import load, dumps


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DIR = os.getcwd()


class Client(object):

    jenkins_path = Path(f'{Path.home()}/.jenkins')

    def __init__(self):
        self.profile = dict()
        self.endpoints = dict()
        self.crumb = dict()

    def _add_profile(self, profile, **kwargs):
        profiles = self._load_profiles()
        profiles[profile] = kwargs
        Client.jenkins_path.write_text(dumps(profiles))

    def _load_profile(self, profile):
        profiles = self._load_profiles()
        return profiles.get(profile, dict())

    def _load_profiles(self):
        if not Client.jenkins_path.is_file():
            return dict()
        return load(Client.jenkins_path.open())

    def _determine_auth(self):
        if self.profile.get('token'):
            return (self.profile['username'], self.profile['token'])
        elif self.profile.get('password'):
            return (self.profile['username'], self.profile['password'])
        else:
            raise Exception('token or password must be provided.')

    def _parse_template_args(self, args):
        arg_pairs = [a.split('=') for a in args]
        return {a[0]: a[1] for a in arg_pairs}

    def _render(self, template_name, **kwargs):
        with open(template_name) as template_file:
            template = Template(template_file.read())
        return template.render(**kwargs)

    def assume(self, profile):
        self.profile = self._load_profile(profile)
        if not self.profile:
            raise Exception('Credentials must be provided via ~/.jenkins')
        self.endpoints = dict(
            crumb=f'{self.profile["url"]}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)',
            script=f'{self.profile["url"]}/scriptText'
        )
        self.crumb = self.authenticate()

    def authenticate(self):
        resp = requests.get(self.endpoints['crumb'], auth=self._determine_auth())
        crumb, status_code = resp.text.split(':'), resp.status_code
        if status_code != 200:
            raise Exception(f'[status_code: {status_code}]')
        return dict(zip(crumb[::2], crumb[1::2]))

    def send(self, script=None, script_path=None):
        if not (script or script_path):
            raise Exception('script or script_path must be provided.')
        if script_path:
            script = Path(script_path).read_text()
        resp = requests.post(
            self.endpoints['script'],
            auth=self._determine_auth(),
            headers=self.crumb,
            data=dict(script=script)
        )
        if resp.status_code != 200:
            raise Exception(f'[status_code: {resp.status_code}]')
        return resp.text


def main():
    args = docopt(__doc__, version='0.0.1')
    client = Client()
    profile = args.get('--profile') or args.get('--url')
    if args.get('auth'):
        client._add_profile(
            profile,
            url=args['--url'],
            username=args['--username'],
            password=args.get('--password'),
            token=args.get('--token')
        )
    client.assume(profile)
    if args.get('send'):
        script_path = args['<file>']
        if not os.path.isabs(script_path):
            script_path = f'{USER_DIR}/{script_path}'
        if args.get('template'):
            kwargs = client._parse_template_args(args['--arg'])
            script = client._render(script_path, **kwargs)
            resp_text = client.send(script=script)
        else:
            resp_text = client.send(script_path=script_path)
    elif args.get('diagnose'):
        resp_text = client.send(script_path=f'{ROOT_DIR}/../scripts/diagnose.groovy')
    elif args.get('ping'):
        resp_text = client.send(script_path=f'{ROOT_DIR}/../scripts/ping.groovy')
    elif args.get('master') and args.get('add'):
        script = client._render(f'{ROOT_DIR}/../templates/add-master.groovy', name=args['<name>'])
        resp_text = client.send(script=script)
    elif args.get('agent-port') and args.get('set'):
        script = client._render(f'{ROOT_DIR}/../templates/set-agent-port.groovy', port=args['<port>'])
        resp_text = client.send(script=script)
    if args.get('--out'):
        Path(args['--out']).write_text(resp_text)
    else:
        print(resp_text)
