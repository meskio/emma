"""
Send a help message

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
from emma.interface.message import Message


class help(Module):
    def run(self):
        cmd_event = Event(event="command")
        subscribe(cmd_event, self.cmd_handler)

    def cmd_handler(self, event, data):
        cmd, args = data[0]
        if cmd != 'help':
            return

        event.event = 'send'
        to = data[1]['From']
        if event.interface == 'irc':
            body = self.help_irc(args)
            if data[1]['To'][0] == '#':
                to = data[1]['To']
        elif event.interface == 'email':
            body = self.help_email(args)
        else:
            body = self.help_none(args)
        msg = Message(body, to)

        trigger(event, msg)

    def help_irc(self, args):
        string = """\
emma is a bot for virtual assembly
==================================
Commands:
- remind 23/11/2011 08:17;hackmeeting@listas.sindominio.ent;subject;text
    Schelude a reminder at certan date
- find From:/hackmeeting/,Tags:asamblea
    Use for search on emails stored by emma
- display 0
    Display an email from a search list generated from 'find'
- moderate
    Start moderating an assembly
- word
    While moderating request word
"""
        return string

    def help_email(self, args):
        string = """\
emma is a bot for virtual assembly

Commands:
- [[remind|23/11/2011 08:17;hackmeeting@listas.sindominio.ent;subject;text]]
Schelude a reminder at certan date
"""
        return string

    def help_none(self, args):
        return "No help"
