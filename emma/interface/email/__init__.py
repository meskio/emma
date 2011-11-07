"""
email interface for mailing lists or private mail

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

import poplib
import smtplib

from emma.interface import Interface
from emma.sched import periodic
from emma.events import Event, trigger, subscribe

from message import Message


class email(Interface):
    def run(self):
        period = self.conf['pop_period']
        periodic(self.fetch, period)
        event = Event(event='send', interface='email', \
                      identifier=self.identifier)
        subscribe(event, self.send_handle)

    def fetch(self):
        self.log("fetching email " + self.conf['pop_user']
                + "@" + self.conf['pop_host'])

        try:
            if self.conf['pop_ssl'] == "yes":
                pop = poplib.POP3_SSL(self.conf['pop_host'])
            else:
                pop = poplib.POP3(self.conf['pop_host'])
            pop.user(self.conf['pop_user'])
            pop.pass_(self.conf['pop_pass'])
        except:
            self.log("    error connecting by POP3")
            return

        recv_event = Event(event='receive', interface='email', \
                           identifier=self.identifier)
        cmd_event = Event(event='command', interface='email', \
                          identifier=self.identifier)
        numMessages = len(pop.list()[1])
        for i in range(numMessages):
            message = Message(pop.retr(i+1)[1])
            trigger(recv_event, message)
            for command in message.commands():
                trigger(cmd_event, (command, message))
            pop.dele(i+1)

        pop.quit()
        self.log("    " + str(numMessages) + " found")

    def send_handle(self, event, msg):
        msg['From'] = self.conf['smtp_address']
        self.send(msg['To'], msg.as_string())

    def send(self, to, msg):
        try:
            if self.conf['smtp_ssl'] == "yes":
                server = smtplib.SMTP_SSL(self.conf['smtp_host'])
            else:
                server = smtplib.SMTP(self.conf['smtp_host'])
            #server.set_debuglevel(1)
            if self.conf['smtp_tls'] == "yes":
                server.starttls()
            server.login(self.conf['smtp_user'], self.conf['smtp_pass'])
        except:
            self.log("    error sending email")
            return

        fromaddr = self.conf['smtp_address']
        server.sendmail(fromaddr, to, msg)
        server.quit()
