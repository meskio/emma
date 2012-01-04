"""
irc interface 

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

import irclib
from time import sleep

from emma.interface import Interface
from emma.events import Event, subscribe, trigger

from ircclient import IrcClient


class irc(Interface):
    def run(self):
        event = Event(event='send', interface='irc',
                      identifier=self.identifier)
        subscribe(event, self.handler)

        server = self.conf['server']
        port = int(self.conf['port'])
        nick = self.conf['nick']
        channel = self.conf['channel']
        self.log("Connect to " + server + ":" + str(port) + " nick:" + nick \
                + " channel:" + channel)

        try:
            self.irc = IrcClient(self.identifier, channel, nick, server, port)
            self.irc.start()
        except irclib.ServerConnectionError, x:
            self.log("error conecting to server: " + x)

    def handler(self, event, data):
        for line in data['Body'].split('\n'):
            self.irc.send(data['To'], line)
            sleep(0.3)    # FIXME: any better way to prevent Flood?
