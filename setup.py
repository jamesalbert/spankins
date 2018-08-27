from setuptools import setup, find_packages

setup(
    name='spankins',
    author='jamesrobertalbert@gmail.com',
    version='0.0.1',
    packages=['spankins'],
    entry_points={
        'console_scripts': [
            'spankins=spankins.__init__:main'
        ]
    }
)
