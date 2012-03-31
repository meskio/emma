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

        help_event = Event(event="help", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(help_event, self.help_handler)
        cmd_event = Event(event="command", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(cmd_event, self.cmd_handler)

    def help_handler(self, event, data):
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
        cmd, args = data[0]
        if data[1]['To'][0] == '#':
            channel = data[1]['To']
        else:
            channel = data[1]['From']

        if cmd == _("find"):
            event = Event("db", "email", self.conf['email_id'])
            search = self.parse_args(args)
            self.log("Find: " + str(search))
            res = run_event(event, search)
            if not res or not res[0]:
                self.say(_("Not found any email"), channel)
            else:
                self.add_search(res[0], channel)
                self.show_list(channel)
        elif cmd == _("display") and channel in self.search:
            emails = self.search[channel]
            try:
                email_index = int(args)
            except ValueError:
                self.say(_("Not valid index: %s") % args, channel)
                return
            if len(emails) > email_index:
                self.show_email(emails[email_index], channel)
            else:
                err_str = (_("Index not in range(0-%(number)d): %(args)s") %
                           {'number':len(emails) - 1, 'args':args})
                self.say(err_str, channel)

    @use_lock
    def add_search(self, emails, channel):
        self.search[channel] = emails

    def show_list(self, channel):
        emails = self.search[channel]
        string = ""
        for i, email in zip(range(len(emails)), emails):
            date = email.get('Date', '')
            frm = email.get('From', '')
            sbj = email.get('Subject', '')
            string += "%d - %s   %s   %s\n" % (i, date, frm, sbj)
        self.say(string, channel)

    def show_email(self, email, channel):
        string = ""
        # We don't need keys translated when searching for them in the
        # email, but they must be translated when presented to the user, so
        # we define a temporal _ function to overwrite builting one.
        # See gettext documentation on deferred translations:
        # http://docs.python.org/library/gettext.html?highlight=gettext#deferred-translations
        def _(msg): return msg
        keys = [_('From'), _('To'), _('Cc'), _('Date'), _('Subject')]
        del _
        for key in keys:
            if key in email:
                string += "%s: %s\n" % (_(key), email[key])
        body = ["   " + line for line in email['Body'].split('\n')]
        string += '\n'.join(body)
        self.say(string, channel)

    def say(self, msg, channel):
        event = Event(event="send", interface="irc", \
                      identifier=self.conf['irc_id'])
        message = Message(msg, channel)
        run_event(event, message)

    def parse_args(self, args):
        #FIXME: improve to take care of spaces
        splited = [item.split(":") for item in args.split(",")]
        return dict(splited)
