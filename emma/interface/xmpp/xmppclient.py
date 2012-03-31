"""
xmpp client

Simple xmpp implementation, is missing a lot of features

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@author: Ales Zabala Alava (Shagi)
@organization: hackmeeting U{http://sindominio.net/hackmeeting}
@contact: shagi@gisa-elkartea.org
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

import re
import logging
import sleekxmpp

from emma.events import Event, subscribe, trigger
from message import Message

class XMPPClient(sleekxmpp.ClientXMPP):
    def __init__(self, identifier, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.identifier = identifier

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, event):
        msg = Message(event)
        self._trigger_rcv(msg)
        self._trigger_cmd(msg)

    def _trigger_rcv(self, msg):
        recv_event = Event(event='receive', interface='xmpp', \
                           identifier=self.identifier)
        trigger(recv_event, msg)

    def _trigger_cmd(self, msg):
        s = msg['Body'].split(" ", 1)
        if len(s) == 2:
            cmd, args = s
        else:
            cmd = s[0]
            args = ""

        logging.info(_("[xmpp %(identifier)s] command received: %(cmd)s: " \
                       "%(args)s") % {'identifier': self.identifier,
                                      'cmd': cmd, 'args': args})
        cmd_event = Event(event='command', interface='xmpp', \
                          identifier=self.identifier)
        trigger(cmd_event, ((cmd, args), msg))

    def send_msg(self, to, msg):
        self.send_message(mto=to,
                          mbody=msg,
                          mtype='chat')
