"""
B{emma}: bot for digital assembly

The code is organice on three layers:
    1. core controls event passing, config file, threads, mutex, storage, ...
    2. L{interface} connect emma to the world (email, irc, wiki, microblog, ...)
    3. L{module} where the actual functionality happens. Easy to program, with
    simple API of events to intercomunicate with the interfaces.

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  http://sam.zoy.org/projects/COPYING.WTFPL for more details.
"""

import thread
import ConfigParser
import re
from time import sleep

from logger import log

confPath = '/usr/local/etc/emma.cfg'
""" Hardcoded the config location, that needs to be fixed """

def main():
    """
    Main function of the program

    It loads all the interfaces and modules described on the config file.
    """
    conf = ConfigParser.RawConfigParser()
    conf.read(confPath)
    log.activate = conf.getboolean("core", "log")

    log("[core] preparing interfaces and modules")
    sectexp = re.compile(r"^[IM] ([^ ]*) (.*)$")
    for section in conf.sections():
        options = dict(conf.items(section))

        m = sectexp.match(section)
        if not m:
            continue
        name, identifier = m.groups()
        if section[0] == 'M':
            log("[core]     load module " + name)
            imp = __import__("emma.module." + name)
            exec "m = imp.module." + name + "." + name \
                    + "('" + identifier + "', options)"
            thread.start_new_thread(m.run, ())
        if section[0] == 'I':
            log("[core]     load interface " + name)
            imp = __import__("emma.interface." + name)
            exec "i = imp.interface." + name + "." + name \
                    + "('" + identifier + "', options)"
            thread.start_new_thread(i.run, ())

    while 1: sleep(1000) # I didn't find any better wait method
