"""
program emails to be sent as reminder

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

from emma.events import Event, subscribe
from emma.sched import at
from emma.module import Module
from emma.interface.message import Message


class reminder(Module):
    def run(self):
        cmd_event = Event(event="command")
        subscribe(cmd_event, self.cmd_handler)

    def cmd_handler(self, event, data):
        cmd, args = data[0]
        if cmd != 'remind':
            return

        s = args.split(';')
        if len(s) == 4:
            date, to, subject, body = s
        elif len(s) == 3:
            date, to, body = s
            subject = "reminder"
        else:
            self.log("args not well formed")
            return

        msg = Message(body, to)
        msg['Subject'] = subject
        send_event = Event('send', self.conf['interface'],
                           self.conf['identifier'])
        at(send_event, msg, date)
