#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'emma',
    version = '0.1dev',
    description = 'Bot for digital assembly',
    author = 'Ruben Pollan',
    author_email = 'meskio@sindominio.net',
    url = 'https://gitorious.org/emma',
    download_url = "https://gitorious.org/emma/emma/archive-tarball/master",
    keywords = ["bot", "email", "irc", "assembly"],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: System Administrators",
        "License :: Public Domain",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Communications :: Email"],
    packages = ['emma',
        'emma.module',
        'emma.module.dummy',
        'emma.module.irc_moderator',
        'emma.module.find_email',
        'emma.interface',
        'emma.interface.email',
        'emma.interface.irc'],
    data_files = [('etc', ['data/emma.cfg'])],
    scripts = ['emm'],
    license = 'WTFPL',
    long_description = open('README').read(),
)
