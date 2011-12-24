"""
B{emma}: bot for digital assembly

The code is organice on three layers:
    1. core controls event passing, config file, threads, mutex, storage, ...
    2. L{interface} connect emma to the world (email, irc, wiki, microblog, ...)
    3. L{module} where the actual functionality happens. Easy to program, with
    simple API of events to intercomunicate with the interfaces.

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@author: Ruben Pollan
@organization: hackmeeting U{http://sindominio.net/hackmeeting}
@contact: meskio@sindominio.net
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

import thread
import ConfigParser
import re
import logging
from time import sleep
from cPickle import loads

from database import DB
from sched import at
from events import Event

version = 0.1
""" Version of emma """

confPath = '/usr/local/etc/emma.cfg'
""" Hardcoded the config location
@note: that needs to be fixed """

def main(conf_path=confPath):
    """
    Main function of the program

    It loads all the interfaces and modules described on the config file.
    """
    conf = ConfigParser.RawConfigParser()
    conf.read(conf_path)
    _init_log(conf)
    db = DB()
    db.connect(conf.get("core", "db_name"))
    core = db.core()
    _load_complements(conf)
    _restore_sched(core)

    while 1: sleep(1000) # I didn't find any better wait method

def _init_log(conf):
    fmt = "%(asctime)s (%(levelname).1s) %(message)s"
    datefmt = "%b %d %H:%M:%S"

    levels = {"debug":    logging.DEBUG,
              "info":     logging.INFO,
              "warning":  logging.WARNING,
              "error":    logging.ERROR,
              "critical": logging.CRITICAL}
    try:
        strlevel = conf.get("core", "log_level")
    except ConfigParser.NoOptionError:
        strlevel = "warning"
    if strlevel in levels:
        level = levels[strlevel]
    else:
        level = logging.WARNING

    try:
        log_file = conf.get("core", "log_file")
        logging.basicConfig(format=fmt, datefmt=datefmt, level=level, \
                            filename=log_file)
    except ConfigParser.NoOptionError:
        logging.basicConfig(format=fmt, datefmt=datefmt, level=level)

    if strlevel not in levels:
        logging.warning("[core] Not valid config value on log_level")

def _load_complements(conf):
    logging.info("[core] preparing interfaces and modules")
    sectexp = re.compile(r"^[IM] ([^ ]*) (.*)$")

    for section in conf.sections():
        options = dict(conf.items(section))
        m = sectexp.match(section)
        if not m:
            continue
        name, identifier = m.groups()
        if section[0] == 'M':
            m = _init_complement('module', name, identifier, options)
            thread.start_new_thread(m.run, ())
        if section[0] == 'I':
            i = _init_complement('interface', name, identifier, options)
            thread.start_new_thread(i.run, ())

def _init_complement(tpe, name, identifier, options):
    db = DB()
    logging.debug("[core]     load %s %s" % (tpe, name))
    db_coll = db.collection("%s_%s_%s" % (tpe, name, identifier))
    imp = __import__("emma.%s.%s" % (tpe, name))
    complements = getattr(imp, tpe)
    complement  = getattr(complements, name)
    clss = getattr(complement, name)
    return clss(identifier, options, db_coll)

def _restore_sched(db):
    sched = db.find({'element': 'sched', 'type': 'at'})
    logging.info("[core] restore " + str(sched.count()) + " scheduled events")
    for s in sched:
        elements = loads(str(s['event']))
        event = Event(*elements)
        data = loads(str(s['data']))
        date = s['date']
        doc_id = s['_id']
        at(event, data, date, doc_id)
