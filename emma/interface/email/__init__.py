"""
email interface for mailing lists or private mail

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

import poplib
import smtplib
import logging
from email.mime.text import MIMEText
from email.utils import parsedate
from time import mktime, sleep
from datetime import datetime

from emma.interface import Interface
from emma.sched import periodic
from emma.events import Event, trigger, subscribe

from message import Message


class email(Interface):
    def run(self):
        """
        Initialize email interface
        """
        self.update_db()
        event = Event(event='send', interface='email', \
                      identifier=self.identifier)
        subscribe(event, self.send_handle)
        sleep(1)  # allow the rest of the interfaces to boot before parse email
        period = self.conf['pop_period']
        periodic(self.fetch, period)

    def fetch(self):
        """
        Fetch email

        Will be run periodically fetching the email from a POP3 server.
        """
        if 'pop_user' in self.conf:
            user = self.conf['pop_user']
            passwd = self.conf['pop_pass']
        elif 'user' in self.conf:
            user = self.conf['user']
            passwd = self.conf['pass']
        else:
            self.log(_("No user defined for pop"), logging.ERROR)
            return

        self.log(_("fetching email %(user)s@%(host)s")
                    % {'user': user, 'host': self.conf['pop_host']})
        try:
            if 'pop_ssl' in self.conf and self.conf['pop_ssl'] == "yes":
                pop = poplib.POP3_SSL(self.conf['pop_host'])
            else:
                pop = poplib.POP3(self.conf['pop_host'])
            pop.user(user)
            pop.pass_(passwd)
        except:
            self.log(_("    error connecting by POP3"), logging.ERROR)
            return

        recv_event = Event(event='receive', interface='email', \
                           identifier=self.identifier)
        cmd_event = Event(event='command', interface='email', \
                          identifier=self.identifier)
        numMessages = len(pop.list()[1])
        for i in range(numMessages):
            message = Message(pop.retr(i + 1)[1])
            trigger(recv_event, message)
            for command in message.commands():
                trigger(cmd_event, (command, message))
            if self.conf['store'] == "yes":
                self.store(message)
            pop.dele(i + 1)

        pop.quit()
        self.log(_("    %s found") % numMessages)

    def send_handle(self, event, msg):
        msg['From'] = self.conf['smtp_address']
        mime = MIMEText(msg['Body'])
        mime['Subject'] = msg['Subject']
        mime['To'] = msg['To']
        self.send(msg['To'], mime.as_string())

    def send(self, to, msg):
        if 'smtp_user' in self.conf:
            user = self.conf['smtp_user']
            passwd = self.conf['smtp_pass']
        elif 'user' in self.conf:
            user = self.conf['user']
            passwd = self.conf['pass']
        else:
            self.log(_("No user defined for smtp"), logging.ERROR)
            return

        try:
            if 'smtp_ssl' in self.conf and self.conf['smtp_ssl'] == "yes":
                server = smtplib.SMTP_SSL(self.conf['smtp_host'])
            else:
                server = smtplib.SMTP(self.conf['smtp_host'])
            if 'smtp_tls' in self.conf and  self.conf['smtp_tls'] == "yes":
                server.starttls()
            server.login(user, passwd)
        except:
            self.log(_("Error sending email"), logging.ERROR)
            return

        fromaddr = self.conf['smtp_address']
        server.sendmail(fromaddr, to, msg)
        server.quit()

    def store(self, message):
        """
        Store message on the database

        @type message: Message
        @param message: message to be stored
        """
        dmsg = dict(message)
        self.db.insert(dmsg)

    def update_db(self):
        old_version, version = Interface.update_db(self)
        if not old_version or old_version == 0.1:
            try:
                res = self.db.find({}, ['_id', 'Date'])
            except Exception:
                self.log(_("db request error."))
                res = []
            for doc in res:
                if not 'Date' in doc:
                    continue
                date = doc['Date']
                if type(date) != unicode:
                    continue
                _id = doc['_id']

                try:
                    timestamp = mktime(parsedate(date))
                except TypeError:
                    self.log(_("time conversion error: %(id)s - %(date)s") %
                             {'id': _id, 'date': date})
                    continue
                utcdate = datetime.fromtimestamp(timestamp)
                try:
                    self.db.update({'_id': _id}, {"$set": {'Date': utcdate}})
                except Exception:
                    self.log(_("db update error: %(id)s - %(date)s") %
                             {'id': _id, 'date': date})

        return (old_version, version)
