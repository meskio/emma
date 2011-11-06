"""
dummy module for testing

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  http://sam.zoy.org/projects/COPYING.WTFPL for more details.
"""

from email.mime.text import MIMEText

from emma.events import Event, subscribe, trigger
from emma.module import Module

class dummy(Module):
    def run(self):
        recv_event = Event(event='receive')
        subscribe(recv_event, self.handler_rcv)
        cmd_event = Event(event='command')
        subscribe(cmd_event, self.handler_cmd)

    def handler_rcv(self, event, message):
        print message['from'] + " -> " + message['to'] + ": " + message['subject']
        print message['tags'] + " " + message['type']
        print message['body']

    def handler_cmd(self, event, data):
        command, message = data
        if command[0] == "print":
            print str(command[1])
        if command[0] == "send":
            msg = MIMEText(command[1])
            msg['Subject'] = "from emma bot"
            msg['To'] = self.conf['send_to']
            send_event = Event(event='send', interface='email', identifier=self.conf['send_id'])
            trigger(send_event, msg)
        if command[0] == "send_irc":
            send_event = Event(event='send', interface='irc', identifier=self.conf['send_id'])
            trigger(send_event, (self.conf['send_chn'], command[1]))
