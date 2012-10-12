"""
xmpp interface

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

from emma.interface import Interface
from emma.events import Event, subscribe

from xmppclient import XMPPClient


class xmpp(Interface):
    def run(self):
        event = Event(event='send', interface='xmpp',
                      identifier=self.identifier)
        subscribe(event, self.handler)

        jid = self.conf['jid']
        password = self.conf['password']
        server = self.conf['server']
        port = int(self.conf['port'])
        self.log(_("Connect to jid: %(jid)s") % self.conf)

        self.xmpp = XMPPClient(self.identifier, jid, password)
        self.xmpp.register_plugin('xep_0030')  # Service Discovery
        self.xmpp.register_plugin('xep_0199')  # XMPP Ping
        if self.xmpp.connect((server, port)):
            self.xmpp.process()
        else:
            self.log(_("error conecting to xmpp: %s") % jid)

    def handler(self, event, data):
        if 'Subject' in data:
            text = "%(Subject)s: %(Body)s" % data
        else:
            text = data['Body']
        self.xmpp.send_msg(data['To'], text)
