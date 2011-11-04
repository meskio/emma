"""
This is a modification of the testbot.py example of the irclib

Simple irc implementation, is missing a lot of features
"""
import re
from ircbot import SingleServerIRCBot

from emma.log import log
from emma.events import Event, subscribe, trigger

from message import Message

class IrcClient(SingleServerIRCBot):
    def __init__(self, identifier, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.nick = nickname
        self.channel = channel
        self.identifier = identifier
        self.cmdexp = re.compile(r"^" + self.nick + r"[:, ] *(.*)$")

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        args = e.arguments()[0]
        msg = Message(e)
        self._trigger_cmd(args, e)

    def on_pubmsg(self, c, e):
        msg = Message(e)
        recv_event = Event(event='receive', interface='irc', \
                           identifier=self.identifier)
        trigger(recv_event, msg)

        # Search for commands
        m = self.cmdexp.match(msg["body"])
        if m:
            args = m.groups()[0]
            self._trigger_cmd(args, msg)

    def send(self, to, msg):
        c = self.connection
        c.privmsg(to, msg)

    def _trigger_cmd(self, args, msg):
        s = args.split(" ", 1)
        if len(s) == 2:
            cmd, args = s
        else:
            cmd = s[0]
            args = ""

        log("[irc " + self.identifier + "] command receved: " + cmd + ": " + args)
        cmd_event = Event(event='command', interface='irc', \
                          identifier=self.identifier)
        trigger(cmd_event, ((cmd, args), msg))