"""
xmpp message support

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

from emma.interface import message


class Message(message.Message):
    """
    xmpp message
    """
    def __init__(self, event):
        body = event['body']
        to = str(event['to'])
        frm = str(event['from'])
        tpe = event['type']
        message.Message.__init__(self, body, to, frm, tpe)
