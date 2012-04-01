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


import time

from emma.events import Event, subscribe, trigger, run_event
from emma.module import Module
from emma.complement import use_lock
from emma.interface.message import Message


class irc_moderator(Module):
    def run(self):
        self.on_moderate = False
        self.session = ''

        help_event = Event(event="help", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(help_event, self.help_handler)
        cmd_event = Event(event="command", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(cmd_event, self.cmd_handler)
        rcv_event = Event(event="receive", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(rcv_event, self.rcv_handler)

    def help_handler(self, event, data):
        if not data:
            return _("  * moderate [session_name]\n" \
                     "    Start moderating an assembly\n" \
                     "  * word\n" \
                     "    While moderating request word\n" \
                     "  * stop\n" \
                     "    Stop moderating\n")
        elif data == _('moderate'):
            return _("Start the moderation of an assembly.\n" \
                     "It will assign turns to talk as people request them" \
                     " with 'word'.\n" \
                     "If a session_name is given the session will be saved " \
                     "on the wiki.")
        elif data == _('word'):
            return _("While moderating request word.\n" \
                     "It can also be requestested with a /me containing the word " \
                     "'word' in it.")
        elif data == _('stop'):
            return _("Stop moderating the assembly started with 'moderate'")
        else:
            return ""

    @use_lock
    def cmd_handler(self, event, data):
        cmd, args = data[0]
        if cmd == _("moderate") and not self.on_moderate:
            self.log(_("starts moderating"))
            self.on_moderate = True
            self.words = []
            self.talking = None
            if args:
                self.session = args
                self.trigger_history('start', args)
            self.send_ctcp(_("starts moderating"))
        elif cmd == _("stop"):
            self.log(_("stops moderating"))
            self.on_moderate = False
            self.wikistore()
            self.session = ''
            self.send_ctcp(_("stops moderating"))
        elif cmd == _("word"):
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
            if data['Type'] == "ctcp" and _("word") in data['Body']:
                nick = data['From']
                self.log(_("Request word from: %s") % nick)
                if self.talking:
                    self.words.append(nick)
                else:
                    self.talking = nick
                    self.give_turn(nick)

    def give_turn(self, nick):
        self.log(_("gives the word to %s") % nick)
        self.send_ctcp(_("gives the word to %s") % nick)

    def send_ctcp(self, txt):
        msg = Message(txt, self.conf['irc_chn'], tpe="ctcp")
        event = Event(event="send", interface="irc",
                      identifier=self.conf['irc_id'])
        trigger(event, msg)

    def trigger_history(self, cmd, param=''):
        event = Event(event="history", interface="irc",
                      identifier=self.conf['irc_id'])
        if cmd in ('start', 'stop'):
            trigger(event, (cmd, param))
        else:
            return run_event(event, (cmd, param))[0]

    def wikistore(self):
        if not self.session:
            return
        if not self.conf.has_key('wiki_id'):
            return

        self.trigger_history('stop')
        self.log(_("Store irc log on the wiki page ") + self.session)

        history = self.trigger_history('get', self.session)
        channel = self.conf['irc_chn']
        today = time.gmtime()
        text = _("Assembly log from %(day)s/%(month)s/%(year)s\n\n") \
                 % {'day': today.tm_mday, 'month': today.tm_mon,
                    'year': today.tm_year}
        text += _("Present: ")
        text += ', '.join(set([msg['From'] for msg in history]))

        text += "\n\n<pre>\n"
        for msg in history:
            if msg['To'] != channel:
                continue
            if msg['Type'] == "ctcp":
                text += "[%s]  * %s %s\n" % (msg['Date'].strftime("%H:%M"),
                                             msg['From'], msg['Body'])
            else:
                text += "[%s] < %s> %s\n" % (msg['Date'].strftime("%H:%M"),
                                             msg['From'], msg['Body'])
        text += "</pre>"

        event = Event(event="write", interface="mediawiki",
                      identifier=self.conf['wiki_id'])
        trigger(event, (self.session, text))
