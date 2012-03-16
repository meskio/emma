"""
mediawiki interface

@copyright: (c) 2012 hackmeeting U{http://sindominio.net/hackmeeting}
@author: Ruben Pollan
@organization: hackmeeting U{http://sindominio.net/hackmeeting}
@contact: meskio@sindominio.net
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""


import mwclient

from emma import __version__
from emma.interface import Interface
from emma.events import Event, trigger, subscribe


class mediawiki(Interface):
    def run(self):
        """
        Initialize mediawiki interface
        """
        host = self.conf['host']
        path = self.conf['path']
        self.wiki = mwclient.Site(host, path)

        user = self.conf['user']
        password = self.conf['password']
        self.wiki.login(user, password)

        event_read = Event(event='read', interface='mediawiki',
                           identifier=self.identifier)
        subscribe(event_read, self.read)
        event_write = Event(event='write', interface='mediawiki',
                           identifier=self.identifier)
        subscribe(event_write, self.write)

    def read(self, event, data):
        return self.wiki.Pages[data].edit()

    def write(self, event, data):
        name, text = data
        page = self.wiki[name]
        page.save(text)
