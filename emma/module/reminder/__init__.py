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
        help_event = Event(event="help")
        subscribe(help_event, self.help_handler)
        cmd_event = Event(event="command")
        subscribe(cmd_event, self.cmd_handler)

    def help_handler(self, event, data):
        if not data:
            if event.interface == "irc":
                return _("  * remind 23/11/2011 08:17;" \
                         "hackmeeting@listas.sindominio.ent;subject;text\n" \
                         "    Schelude a reminder at certan date\n")
            elif event.interface == "email":
                return _("  * [[remind|23/11/2011 08:17;" \
                         "hackmeeting@listas.sindominio.ent;subject;text]]\n" \
                         "    Schelude a reminder at certan date\n")
        elif data[0] == _('remind'):
            return _("You can program reminders to be send by %s at a " \
                     "given date.\n It takes three or four parameters " \
                     "separated by ';': date;email;subject;body\n" \
                     "The subject is optional") % (self.conf['interface'])
        return ""

    def cmd_handler(self, event, data):
        cmd, args = data[0]
        if cmd != _('remind'):
            return

        s = args.split(';')
        if len(s) == 4:
            date, to, subject, body = s
        elif len(s) == 3:
            date, to, body = s
            subject = _("reminder")
        else:
            self.log(_("args not well formed"))
            return

        msg = Message(body, to)
        msg['Subject'] = subject
        send_event = Event('send', self.conf['interface'],
                           self.conf['identifier'])
        at(send_event, msg, date)
