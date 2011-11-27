"""
Loggin system for emma

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

_log_lock = thread.allocate_lock()

def log(msg):
    """
    Output a log string

    If activated it prompts the string to the standard output. It can be
    activated or deactivated by the config file, with the variable 'log' on the
    'core' section. L{interface} and L{module} should use the
    L{Complement.log()<emma.complement.Complement.log>} method, wich is inhered
    to the class.

    The log can be activate or deactibate by setting log.activate variable to
    True or False

    @type msg: string
    @param msg: the text to output, usually on the form:
        "[complement_name identifier] text"
    """
    global activate

    if log.activate:
        with _log_lock: print msg
