"""
email message support

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

from email.feedparser import FeedParser
import email.message
import re

from emma.interface import message

class Message(message.Message):
    """
    email message

    All the headers apears on the dictionary as msg[hdr_name]. The attachments
    are a list on the msg['attachments'].
    """
    def __init__(self, list_lines):
        p = FeedParser()
        for line in list_lines:
            p.feed(line + "\n")
        self.message = p.close()

        frm = self.message['from']
        to = self.message['to']
        payload = self.message.get_payload()
        if type(payload) == list:
            body = payload[0].get_payload()
        else:
            body = payload
        attachments = payload
        message.Message.__init__(self, frm, to, body, 'email')
        self._['attachments'] = attachments

        self.lines = list_lines
        self.comexp = re.compile(r"\[\[([^\|]*)\|([^\]]*)\]\]")
        self.tagexp = re.compile(r"\[([^\]]*)\]")

    def __getitem__(self, item):
        if item in self._:
            return self._[item]
        elif item == 'commands':
            return self.commands()
        elif item == 'tags':
            return self.tags()
        elif item in self.message:
            return self.message[item]
        else:
            return ""

    def commands(self):
        """
        get a list of the commands inside the email

        Everithing with the form [[cmd|params]] will be reconice as command

        @returns: [(cmd, params)]
        """
        text = self['body']
        return self.comexp.findall(text)

    def tags(self):
        """
        get a list of the tags from the subject

        The text between [ and ] is consider as a tag

        @returns: [tag]
        """
        subject = self['subject']
        return self.tagexp.findall(subject)
