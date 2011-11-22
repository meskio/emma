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


class find_email(Module):
    def run(self):
        cmd_event = Event(event="command", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(cmd_event, self.cmd_handler)

    def cmd_handler(self, event, data):
        cmd, args = data[0]
        if cmd != "find":
            return

        event = Event("db", "email", self.conf['email_id'])
        search = self.parse_args(args)
        self.log("Find: " + str(search))
        res = run_event(event, search)
        if not res or not res[0].count():
            self.say("Not found any email", data[1]['From'])
        else:
            for email in res[0]:
                self.show_email(email, data[1]['From'])

    def show_email(self, email, channel):
        for key in ['From', 'To', 'Cc', 'Date', 'Subject']:
            if key in email:
                self.say(key + ": " + email[key], channel)
        body = [ "|  " + line for line in email['Body'].split('\n') ]
        for line in body:
            self.say(line, channel)

    def say(self, msg, channel):
        event = Event(event="send", interface="irc", \
                      identifier=self.conf['irc_id'])
        run_event(event, (channel, msg))
        sleep(0.4) #FIXME: any better way to prevent Flood?

    def parse_args(self, args):
        #FIXME: improve to take care of spaces
        splited = [ item.split(":") for item in args.split(",") ]
        return dict(splited)
