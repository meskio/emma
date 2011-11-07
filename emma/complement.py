"""
The necessary class and decorators for L{interface} and L{module}

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

import thread

from logger import log

def use_lock(fn):
    """
    Decorator for add a lock to a method

    It decorates methods of child classes of L{Complement}, usually L{interface}
    or L{module}. Adds the use of a locker (mutex) to the method, so the access
    to the class data is thread safe.
    
    >>> from emma.complement import use_lock
    >>> class myModule(Module):
    ...     @use_lock
    ...     def run(self):
    ...         self.var = 0
    ...     
    ...     @use_lock
    ...     def inc(self):
    ...         self.var += 1
    """
    def wrapper(self, *arg):
        self.lock.acquire()
        res = fn(self, *arg)
        self.lock.release()
        return res
    return wrapper

class Complement:
    """
    Empty class mented to be inhered by L{interface} and L{module}

    It handles the configuration, identifier and locker.
    """
    def __init__(self, identifier, conf):
        """
        @type identifier: string
        @param identifier: complement unique identifier, on L{interface} it is
            use for the L{Event} invocation
        @type conf: dictionary
        @param conf: the configuration of the module as {item: value}
        """
        self.conf = conf
        self.identifier = identifier
        self.lock = thread.allocate_lock()

    def run(self):
        """
        The starting method of the complement

        Each L{interface} or L{module} should define here the initialization,
        L{subscribe<emma.events.subscribe>} to events, the 
        L{periodic<emma.sched.periodic>} actions, ...
        """
        pass

    def log(self, msg):
        """
        Output a log string

        If loggin activated prompts on standard output the string adding to it
        "[complement_name identifier] ". Uses L{emma.logger.log()}.

        @type msg: string
        @param msg: the text to output
        """
        name = self.__module__.split(".")[-1]
        log("[" + name + " " + self.identifier + "] " + msg)
