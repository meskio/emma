"""
irc message support

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  http://sam.zoy.org/projects/COPYING.WTFPL for more details.
"""

from irclib import nm_to_n

class Message:
    def __init__(self, ircEvent):
        self._body = ircEvent.arguments()[0]
        self._nick = nm_to_n(ircEvent.source())
        self._to = ircEvent.target()
        self._type = ircEvent.eventtype()

    def __getitem__(self, item):
        if item == 'body':
            return self._body
        elif item == 'from':
            return self._nick
        elif item == 'to':
            return self._to
        elif item == 'type':
            return self._type
        else:
            return ""
