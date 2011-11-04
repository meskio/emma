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
