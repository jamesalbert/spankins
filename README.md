# spankins
**s**end **pa**in to Je**nkins**

**s**tored **p**rofiles **a**nd  Je**nkins**

Spankins is a great word.

## Application

```
spankins

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
```

## Installation

`pip install spankins`

## Quickstart

Spankins makes interfacing with multiple jenkins instances easy with profiles. Credentials are stored locally in plain-text (totally legit).

```
$ spankins auth --url=https://jenkins.me.com --username=jalbert@me.com --token=JHH34JHLJ3H43LH3 --profile=myJenkins
$ cat ~/.jenkins | jq
{
  "myJenkins": {
    "url": "https://jenkins.me.com",
    "username": "jalbert@me.com",
    "password": null,
    "token": "JHH34JHLJ3H43LH3"
  }
}
$ # spankins provides a few helper scripts
$ spankins ping --profile=myJenkins
pong

$ spankins master add newMaster --profile=myJenkins
Created ClientMaster 'newMaster' known as '0-newMaster'
-DMASTER_INDEX=0'
-DMASTER_NAME=newMaster'
-DMASTER_GRANT_ID=6049b0a1-0dbb-4d01-aa02-4e60de514590'

$ # you can also send your own script (note the difference between `send` and `send template`)
$ spankins send ./scripts/bitcoin.groovy --profile=myJenkins --out=./logs/bitcoin.log
$ # if you have a jinja2-templated groovy script: println("Good {{ when }}, {{ name }}")
$ spankins send template ./templates/greet.groovy --arg=name=Penny --arg=when=afternoon --profile=myJenkins
Good afternoon, Penny
```
