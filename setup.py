from __future__ import print_function

from glob import glob

try:
    from setuptools import setup
except ImportError:
    print("Falling back to distutils. Functionality may be limited.")
    from distutils.core import setup

requires = []
long_description = open('README.rst').read() + "\n\n" + open("Changelog").read()

config = {
    'name'            : 'rogers-usage',
    'description'     : '''Scrape information from a My Rogers account, format it
                        into an email, and send it to a recipient.''',
    'long_description': long_description,
    'author'          : 'Brandon Sandrowicz',
    'author_email'    : 'brandon@sandrowicz.org',
    'url'             : 'https://github.com/bsandrow/rogers-usage',
    'version'         : '0.1',
    'packages'        : ['rogers_usage'],
    'package_data'    : { '': ['LICENSE'] },
    'scripts'         : glob('bin/*'),
    'install_requires': requires,
    'license'         : open('LICENSE').read(),
    'test_suite'      : '',
    'classifiers'     : (,
    ),
}

setup(**config)
