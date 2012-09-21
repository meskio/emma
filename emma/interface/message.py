"""
generic message for interfaces

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

from datetime import datetime


class Message(dict):
    """
    Message is basically a dictionary
    """
    def __init__(self, body=None, to=None, frm=None, tpe=None,
                 date=datetime.utcnow()):
        """
        @type body: string
        @param body: content
        @type to: string
        @param to: target
        @type frm: string
        @param frm: source
        @type tpe: string
        @param tpe: message type
        @type date: datetime
        @param date: message date
        """
        super(Message, self).__init__(From=frm, To=to, Body=body, Type=tpe,
                                     Date=date)

    def __getitem__(self, item):
        if item not in self:
            return ""
        else:
            return super(Message, self).__getitem__(item)
