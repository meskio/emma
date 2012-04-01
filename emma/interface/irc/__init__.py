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

import logging
import irclib
from time import sleep

from emma.interface import Interface
from emma.events import Event, subscribe, trigger

from ircclient import IrcClient


class irc(Interface):
    def run(self):
        event_send = Event(event='send', interface='irc',
                      identifier=self.identifier)
        subscribe(event_send, self.send_handler)
        event_history = Event(event='history', interface='irc',
                              identifier=self.identifier)
        subscribe(event_history, self.history_handler)
        event_rcv = Event(event='receive', interface='irc',
                              identifier=self.identifier)
        subscribe(event_rcv, self.rcv_handler)

        self.store = ''
        self.update_db()
        server = self.conf['server']
        port = int(self.conf['port'])
        nick = self.conf['nick']
        channel = self.conf['channel']
        self.log(_("Connect to %(server)s:%(port)s nick:%(nick)s " \
                   "channel:%(channel)s") % self.conf)

        try:
            self.irc = IrcClient(self.identifier, channel, nick, server, port)
            self.irc.start()
        except irclib.ServerConnectionError, x:
            self.log(_("error conecting to server: %s") % x)

    def send_handler(self, event, data):
        for line in data['Body'].split('\n'):
            self.irc.send(data['To'], line, data['Type'])
            sleep(0.3)    # FIXME: any better way to prevent Flood?

    def history_handler(self, event, data):
        if data[0] == 'start':
            self.store = data[1]
        elif data[0] == 'stop':
            self.store = ''
        elif data[0] == 'get':
            name = data[1]
            try:
                res = self.db.find({'session': name})
            except Exception:
                self.log(_("db request error."))
                res = []
            return [i for i in res]
        else:
            self.log(_("Not valid command for history: ") + data[0],
                     logging.ERROR)

    def rcv_handler(self, event, data):
        if not self.store:
            return

        dmsg = dict(data)
        dmsg['session'] = self.store
        self.db.insert(dmsg)
