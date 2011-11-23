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

class Message:
    """
    Message is basically a dictionary
    """
    def __init__(self, body=None, to=None, frm=None, tpe=None):
        """
        @type body: string
        @param body: content
        @type to: string
        @param to: target
        @type frm: string
        @param frm: source
        @type tpe: string
        @param tpe: message type
        """
        self._ = {'From': frm, 'To': to, 'Body': body, 'Type': tpe}

    def items(self):
        return self._.items()

    def __getitem__(self, item):
        if item in self._:
            return self._[item]
        else:
            return ""

    def __setitem__(self, item, value):
        self._[item] = value

    def __iter__(self):
        class __meta__:
            def __init__(self, elements):
                self.elements = elements

            def next(self):
                if len(self.elements):
                    element = self.elements[0]
                    self.elements = self.elements[1:]
                    return element
                else:
                    raise StopIteration
        return __meta__(self.items())
