"""
simple issue tracker module

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
from emma.complement import use_lock
from emma.interface.message import Message


class issues(Module):
    def run(self):
        self.todo_list = []

        help_event = Event(event="help", identifier=self.conf['id'])
        subscribe(help_event, self.help_handler)
        cmd_event = Event(event="command", identifier=self.conf['id'])
        subscribe(cmd_event, self.cmd_handler)

    def help_handler(self, event, data):
        if not data:
            return _("  Keep track of issues.\n" \
                     "  * issues [group]\n" \
                     "    Show issues. If group given, filter by it.\n" \
                     "  * issue group bla\n" \
                     "    Add new issue, required by the group\n" \
                     "  * done n\n" \
                     "    close issue numbered with n in issue list.\n")
        elif data[0] == _('issues'):
            return _("Show the list of issues.")
        elif data[0] == _('issue'):
            return _("Add new issue")
        elif data[0] == _('done'):
            return _("Close the issue'")
        else:
            return ""

    def cmd_handler(self, event, data):
        cmd, args = data[0]
        if cmd == _("issues"):
            self.issues(event, data)
        elif cmd == _("issue"):
            self.issue(event, data)
        elif cmd == _("done"):
            self.done(event, data)

    def issue(self, event, data):
        cmd, args = data[0]
        if event.interface == "email":
            group, text = args.split("\n", 1)
        else:
            group, text = args.split(" ", 1)
        self.db.insert({"group": group, "text": text})

        # Reply ack
        to = data[1]['From']
        if event.interface == 'irc' and data[1]['To'][0] == '#':
            to = data[1]['To']
        msg = Message(_("issue accepted"), to)
        event = Event(event="send", interface=event.interface,
                      identifier=event.identifier)
        trigger(event, msg)
        self.log(_("Issue accepted (%s, %s)") % (group, text))

    def issues(self, event, data):
        pass

    def done(self, event, data):
        pass
