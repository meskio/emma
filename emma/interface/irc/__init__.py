import irclib

from emma.interface import Interface
from emma.events import Event, subscribe, trigger

from ircclient import IrcClient

class irc(Interface):
    def run(self):
        event = Event(event='send', interface='irc', identifier=self.identifier)
        subscribe(event, self.handler)

        server = self.conf['server']
        port = int(self.conf['port'])
        nick = self.conf['nick']
        channel =  self.conf['channel']
        self.log("Connect to " + server + ":" + str(port) + " nick:" + nick \
                + " channel:" + channel)

        try:
            self.irc = IrcClient(self.identifier, channel, nick, server, port)
            self.irc.start()
        except irclib.ServerConnectionError, x:
            self.log("error conecting to server: " + x)

    def handler(self, event, data):
        self.irc.send(data[0], data[1])

