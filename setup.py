#!/usr/bin/env python

from distutils.core import setup

setup(
    name='asambleitor',
    version='0.1dev',
    description='Bot for digital assembly',
    author='hackmeeting',
    url='http://sindominio.net/hackmeeting',
    packages=['asambleitor',
        'asambleitor.core',
        'asambleitor.module',
        'asambleitor.module.dummy',
        'asambleitor.interface',
        'asambleitor.interface.email'],
    data_files=[('etc', ['data/asambleitor.cfg'])],
    scripts=['asamtor'],
    license='WTFPL',
    long_description=open('README').read(),
)
