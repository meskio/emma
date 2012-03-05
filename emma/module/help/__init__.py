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

from emma.events import Event, subscribe, trigger, run_event
from emma.module import Module
from emma.interface.message import Message


class help(Module):
    def run(self):
        cmd_event = Event(event="command")
        subscribe(cmd_event, self.cmd_handler)

    def cmd_handler(self, event, data):
        cmd, args = data[0]
        # Accept also untranslated help, at least this command should work
        # always :-)
        if cmd not in ('help', _('help')):
            return

        # Gather help messages from modules
        event.event = 'help'
        help_strs = set(run_event(event, data[0][1]))
        help_strs -= set("")
        if help_strs:
            body = _("emma is a bot for virtual assembly\n" \
                     "==================================\n" \
                     "Commands:\n")
            body += '\n'.join(help_strs)
        else:
            body = _("No help")

        event.event = 'send'
        to = data[1]['From']
        if event.interface == 'irc' and data[1]['To'][0] == '#':
            to = data[1]['To']
        msg = Message(body, to)
        msg['Subject'] = _("help")
        trigger(event, msg)
