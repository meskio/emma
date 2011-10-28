#!/usr/bin/env python

from distutils.core import setup

setup(
    name='emma',
    version='0.1dev',
    description='Bot for digital assembly',
    author='hackmeeting',
    url='http://sindominio.net/hackmeeting',
    packages=['emma',
        'emma.module',
        'emma.module.dummy',
        'emma.interface',
        'emma.interface.email'],
    data_files=[('etc', ['data/emma.cfg'])],
    scripts=['emm'],
    license='WTFPL',
    long_description=open('README').read(),
)
