#!/usr/bin/env python

from distutils.core import setup, Command

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtest.py'])
        raise SystemExit(errno)

setup(
    name = 'emma',
    version = '0.2',
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
        'emma.module.irc_moderator',
        'emma.module.find_email',
        'emma.module.reminder',
        'emma.module.email2wiki',
        'emma.module.help',
        'emma.interface',
        'emma.interface.email',
        'emma.interface.irc',
        'emma.interface.mediawiki',
        'emma.interface.xmpp'],
    package_data={'emma': ['locale/*/*/*']},
    data_files = [('etc/init.d', ['data/init.d/emma']),
                  ('etc', ['data/emma.cfg'])],
    scripts = ['emm', 'bin/mbox2emma'],
    license = 'WTFPL',
    long_description = open('README').read(),
    cmdclass = {'test': PyTest},
)
