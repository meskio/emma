"""
find an email from irc

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

from time import sleep

from emma.events import Event, subscribe, run_event
from emma.module import Module
from emma.complement import use_lock


class find_email(Module):
    def run(self):
        self.search = {}
        """ {channel:[email]} """

        cmd_event = Event(event="command", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(cmd_event, self.cmd_handler)

    def cmd_handler(self, event, data):
        cmd, args = data[0]
        if data[1]['To'][0] == '#':
            channel = data[1]['To']
        else:
            channel = data[1]['From']

        if cmd == "find":
            event = Event("db", "email", self.conf['email_id'])
            search = self.parse_args(args)
            self.log("Find: " + str(search))
            res = run_event(event, search)
            if not res or not res[0]:
                self.say("Not found any email", channel)
            else:
                self.add_search(res[0], channel)
                self.show_list(channel)
        elif cmd == "display" and channel in self.search:
            emails = self.search[channel]
            try:
                email_index = int(args)
            except ValueError:
                self.say("Not valid index: " + args, channel)
                return
            if len(emails) > email_index:
                self.show_email(emails[email_index], channel)
            else:
                err_str = "Index not in range(0-%d): %s" % (len(emails)-1, args)
                self.say(err_str, channel)

    @use_lock
    def add_search(self, emails, channel):
        self.search[channel] = emails

    def show_list(self, channel):
        emails = self.search[channel]
        for i, email in zip(range(len(emails)), emails):
            date = email.get('Date', '')
            frm = email.get('From', '')
            sbj = email.get('Subject', '')
            line = "%d - %s   %s   %s" % (i, date, frm, sbj)
            self.say(line, channel)

    def show_email(self, email, channel):
        for key in ['From', 'To', 'Cc', 'Date', 'Subject']:
            if key in email:
                self.say(key + ": " + email[key], channel)
        body = [ "   " + line for line in email['Body'].split('\n') ]
        for line in body:
            self.say(line, channel)

    def say(self, msg, channel):
        event = Event(event="send", interface="irc", \
                      identifier=self.conf['irc_id'])
        run_event(event, (channel, msg))
        sleep(0.3) #FIXME: any better way to prevent Flood?

    def parse_args(self, args):
        #FIXME: improve to take care of spaces
        splited = [ item.split(":") for item in args.split(",") ]
        return dict(splited)
