"""
irc moderator module

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

from emma.events import Event, subscribe, trigger
from emma.module import Module
from emma.complement import use_lock
from emma.interface.message import Message


class irc_moderator(Module):
    def run(self):
        self.on_moderate = False

        cmd_event = Event(event="command", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(cmd_event, self.cmd_handler)
        rcv_event = Event(event="receive", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(rcv_event, self.rcv_handler)

    @use_lock
    def cmd_handler(self, event, data):
        cmd, args = data[0]
        self.log("hau da komandoa: "+cmd)
        if cmd == "moderate" and not self.on_moderate:
            self.log(_("Start moderating"))
            self.on_moderate = True
            self.words = []
            self.talking = None
        elif cmd == "stop":
            self.log(_("Stop moderating"))
            self.on_moderate = False
        elif cmd == "word":
            nick = data[1]['From']
            self.log(_("Request word from: %s") % nick)
            if self.talking:
                self.words.append(nick)
            else:
                self.talking = nick
                self.give_turn(nick)

    @use_lock
    def rcv_handler(self, event, data):
        if self.on_moderate:
            if data['Body'] == "." and data['From'] == self.talking:
                if self.words:
                    self.talking = self.words[0]
                    self.words = self.words[1:]
                    self.give_turn(self.talking)
                else:
                    self.talking = None

    def give_turn(self, nick):
        self.log(_("Give word to: %s") % nick)
        msg = Message(_("%s has the word") % nick, self.conf['irc_chn'])
        event = Event(event="send", interface="irc", \
                      identifier=self.conf['irc_id'])
        trigger(event, msg)
