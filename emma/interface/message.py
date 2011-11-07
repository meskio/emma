"""
generic message for interfaces

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

class Message:
    """
    Message is basically a dictionary
    """
    def __init__(self, frm=None, to=None, body=None, tpe=None):
        """
        @type frm: string
        @param frm: source
        @type to: string
        @param to: target
        @type body: string
        @param body: content
        @type tpe: string
        @param tpe: message type
        """
        self._ = {'from': frm, 'to': to, 'body': body, 'type': tpe}

    def __getitem__(self, item):
        if item in self._:
            return self._[item]
        else:
            return ""

    def __setitem__(self, item, value):
        self._[item] = value
