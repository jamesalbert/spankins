from setuptools import setup, find_packages

setup(
    name='spankins',
    author='jamesrobertalbert@gmail.com',
    version='0.0.2',
    url='https://github.com/jamesalbert/spankins',
    long_description='',
    packages=['spankins'],
    install_requires=[
        'docopt',
        'requests',
        'jinja2'
    ],
    entry_points={
        'console_scripts': [
            'spankins=spankins.__init__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)
