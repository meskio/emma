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

        help_event = Event(event="help", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(help_event, self.help_handler)
        cmd_event = Event(event="command", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(cmd_event, self.cmd_handler)
        rcv_event = Event(event="receive", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(rcv_event, self.rcv_handler)

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

    @use_lock
    def cmd_handler(self, event, data):
        cmd, args = data[0]
        if cmd == _("issues"):
            pass
        elif cmd == _("issue"):
            pass
        elif cmd == _("done"):
            pass

    @use_lock
    def rcv_handler(self, event, data):
        if self.on_moderate:
            if data['Body'] == "." and data['From'] == self.talking:
                if self.words:
                    self.talking = self.words[0]
                    self.words = self.words[1:]
                    self.give_turn(self.talking)
                else:
                    self.talking = None

    def give_turn(self, nick):
        self.log(_("Give word to: %s") % nick)
        msg = Message(_("%s has the word") % nick, self.conf['irc_chn'])
        event = Event(event="send", interface="irc", \
                      identifier=self.conf['irc_id'])
        trigger(event, msg)
