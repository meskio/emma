"""
email -> Wiki bridge

The commands sent by email with wiki markup will be stored on the wiki page
with the given name

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


class email2wiki(Module):
    def run(self):
        help_event = Event(event="help", interface="email",
                           identifier=self.conf['email_id'])
        subscribe(help_event, self.help_handler)
        cmd_event = Event(event="command", interface="email",
                          identifier=self.conf['email_id'])
        subscribe(cmd_event, self.cmd_handler)


    def help_handler(self, event, data):
        if not data:
            return _("  * [[wiki|wiki page name\n" \
                     "      text on wiki markup]]\n" \
                     "    Store the text on the wiki page\n")
        elif data == _('wiki'):
            return _("The arguments up to the first change of line will" \
                     "be considered the name of the page on the wiki\n" \
                     "to create or change with the text given after the" \
                     "first change of line")
        return ""

    def cmd_handler(self, event, data):
        cmd, args = data[0]
        page, text = args.split("\n", 1)
        page = page.strip()
        event_write = Event(event='write', interface='mediawiki',
                            identifier=self.conf['wiki_id'])
        self.log(_("Store '%s' page on the '%s' wiki")
                    % (page, self.conf['wiki_id']))
        trigger(event_write, (page, text))
