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
        msg = p.close()
        
        if 'Content-Type' in msg:
            exp = re.compile(r"charset=([^;]*)")
            charset = exp.findall(msg['Content-Type'])[0]

        payload = msg.get_payload()
        if type(payload) == list:
            body = payload[0].get_payload()
            attachments = payload
        else:
            body = payload
            attachments = [payload]
        if charset:
            body = body.decode(charset).encode("UTF-8")
            attachments = [ at.decode(charset).encode("UTF-8") for at in attachments ]
        message.Message.__init__(self, body=body, tpe='email')
        self._['attachments'] = attachments

        for key, value in msg.items():
            key = key.lower()
            if charset:
                value = value.decode(charset).encode("UTF-8")
            self._[key] = value

        self._['commands'] = self.commands()
        self._['tags'] = self.tags()

    def commands(self):
        """
        get a list of the commands inside the email

        Everithing with the form [[cmd|params]] will be reconice as command

        @returns: [(cmd, params)]
        """
        comexp = re.compile(r"\[\[([^\|]*)\|([^\]]*)\]\]")
        text = self['body']
        return comexp.findall(text)

    def tags(self):
        """
        get a list of the tags from the subject

        The text between [ and ] is consider as a tag

        @returns: [tag]
        """
        tagexp = re.compile(r"\[([^\]]*)\]")
        subject = self['subject']
        return tagexp.findall(subject)
