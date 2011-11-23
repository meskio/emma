"""
interfaces are where the comunication to the internet happends

Interfaces communicate with L{modules<module>} through L{events}. modules 
will do the functionallity of the bot, using interfaces for communicate with
mailing lists, irc, ...

Interface inheritate from L{complement} from where you can
L{log<emma.complement.Complement.log>}, L{use locks<emma.complement.use_lock>},
... Everything in an interface happens in parallel on several threads, so for
class variables L{locks<emma.complement.use_lock>} should be use.

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

import re

from emma.complement import Complement
from emma.events import Event, subscribe


class Interface(Complement):
    def __init__(self, *args):
        Complement.__init__(self, *args)
        name = self.__module__.split(".")[-1]
        event = Event(event="db", interface=name, identifier=self.identifier)
        subscribe(event, self.db_handler)

    def db_handler(self, event, data):
        """
        Default DB handler

        Get a database search for the collection of the interface and return
        it's results.

        @type event: l{event}
        @param event: event to be triggered, it must have all the elements
        @type data: dict
        @param data: a db search, like {"type": "foo", "body": True}
        @returns: results of the db search
        """
        search = {}
        for k, v in data.items():
            if '/' == v[0] == v[-1]:
                search[k] = re.compile(v[1:-2])
            else:
                search[k] = v

        try:
            res = self.db.find(search)
        except Exception:
            self.log("db request error.")
            res = []
        return [ i for i in res ]

