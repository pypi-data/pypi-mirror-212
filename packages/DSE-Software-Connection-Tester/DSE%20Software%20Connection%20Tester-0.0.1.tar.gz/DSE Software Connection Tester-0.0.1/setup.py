from setuptools import setup, find_packages

VERSION = '0.0.1'
NAME = 'DSE Software Connection Tester'
DESCRIPTION = 'A connection testing package.'
LONG_DESCRIPTION = 'A package that allows for testing the resolvability of a domain name ' \
                   'and the accessibility of an ip address.'
AUTHOR = 'Gabi Barrientos de Reus'
AUTHOR_EMAIL = 'gabi@dsesoftware.nl'


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    requires=['subprocess', 'logging', 'http', 'enum', 'os', 'typing'],
    keywords=['DSE Software', 'connection', 'dns', 'resolve', 'ping'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows'
    ]
)

