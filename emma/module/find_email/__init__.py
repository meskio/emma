"""
find an email from irc

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

from emma.events import Event, subscribe, run_event
from emma.module import Module
from emma.complement import use_lock
from emma.interface.message import Message


class find_email(Module):
    def run(self):
        self.search = {}
        """ {channel:[email]} """

        help_event = Event(event="help", identifier=self.conf['im_id'])
        subscribe(help_event, self.help_handler)
        cmd_event = Event(event="command", identifier=self.conf['im_id'])
        subscribe(cmd_event, self.cmd_handler)

    def help_handler(self, event, data):
        if not event.interface in ["irc", "xmpp"]:
            return ""

        if not data:
            return _("  * find From:/hackmeeting/,Tags:asamblea\n" \
                     "    Use for search on emails stored by emma\n" \
                     "  * display 0\n" \
                     "    Display an email from a search list generated\n")
        elif data == _('find'):
            return _("Use for search on emails stored by emma.\n" \
                     "Search terms are introduced separated by ','" \
                     "with the form 'Field:string',\n" \
                     "string can be a regular expression between '/'.\n" \
                     "Ex: find From:/meskio.*/,Tags:asamblea,Body:/squat/")
        elif data == _('display'):
            return _("Once a 'find' command is call use the 'display'" \
                     "command to output the email\n" \
                     "with the index number give as parameter of 'display'\n" \
                     "Ex: display 0")
        else:
            return ""

    def cmd_handler(self, event, data):
        interface = event.interface
        if not interface in ["irc", "xmpp"]:
            return

        cmd, args = data[0]
        to = data[1]['From']
        if interface == 'irc' and data[1]['To'][0] == '#':
            to = data[1]['To']

        if cmd == _("find"):
            event = Event("db", "email", self.conf['email_id'])
            search = self.parse_args(args)
            self.log("Find: " + str(search))
            res = run_event(event, search)
            if not res or not res[0]:
                self.say(_("Not found any email"), to, interface)
            else:
                self.add_search(res[0], to)
                self.show_list(to, interface)
        elif cmd == _("display") and to in self.search:
            emails = self.search[to]
            try:
                email_index = int(args)
            except ValueError:
                self.say(_("Not valid index: %s") % args, to, interface)
                return
            if len(emails) > email_index:
                self.show_email(emails[email_index], to, interface)
            else:
                err_str = (_("Index not in range(0-%(number)d): %(args)s") %
                           {'number': len(emails) - 1, 'args': args})
                self.say(err_str, to, interface)

    @use_lock
    def add_search(self, emails, channel):
        self.search[channel] = emails

    def show_list(self, channel, interface):
        emails = self.search[channel]
        string = ""
        for i, email in zip(range(len(emails)), emails):
            date = email.get('Date', '')
            frm = email.get('From', '')
            sbj = email.get('Subject', '')
            string += "%d - %s   %s   %s\n" % (i, date, frm, sbj)
        self.say(string, channel, interface)

    def show_email(self, email, channel, interface):
        string = ""
        # We don't need keys translated when searching for them in the
        # email, but they must be translated when presented to the user, so
        # we define a temporal _ function to overwrite builting one.
        # See gettext documentation on deferred translations:
        # http://docs.python.org/library/gettext.html?highlight=gettext#deferred-translations
        def N_(msg): return msg
        keys = [N_('From'), N_('To'), N_('Cc'), N_('Date'), N_('Subject')]
        for key in keys:
            if key in email:
                string += "%s: %s\n" % (_(key), email[key])
        body = ["   " + line for line in email['Body'].split('\n')]
        string += '\n'.join(body)
        self.say(string, channel, interface)

    def say(self, msg, channel, interface):
        event = Event(event="send", interface=interface, \
                      identifier=self.conf['im_id'])
        message = Message(msg, channel)
        run_event(event, message)

    def parse_args(self, args):
        #FIXME: improve to take care of spaces
        splited = [item.split(":") for item in args.split(",")]
        return dict(splited)
