from emma.interface import interface
from emma.log import log
from emma.events import Event, subscribe, trigger

from ircclient import IrcClient

class irc(interface):
    def run(self):
        server = self.conf['server']
        port = self.conf['port']
        nick = self.conf['nick']
        channel =  self.conf['channel']

        try:
            self.irc = IrcClient(channel, nick, server, port)
        except irclib.ServerConnectionError, x:
            log("[irc] error conecting to server: " + x)
        self.irc.start()

        event = Event(interface='irc', identifier=self.identifier)
        subscribe(Event, self.handler)

    def handler(self, event, data):
        event_type, data = do_command() #TODO
        e = Event(event=event_type, interface='irc', identifier=self.identifier)
        trigger(e, data)

