"""
email message support

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

import pyzmail
#from email.feedparser import FeedParser
#import email.message
import re

from emma.interface import message

class Message(message.Message):
    """
    email message

    All the headers apears on the dictionary as msg[hdr_name]. The attachments
    are a list on the msg['attachments'].
    """
    def __init__(self, list_lines):
        message.Message.__init__(self, tpe='email')

        msgStr = '\n'.join(list_lines)
        msg = pyzmail.PyzMessage.factory(msgStr)

        d = _msg_to_dict(msg)
        self._.update(d)
        self._['Commands'] = self.commands()
        self._['Tags'] = self.tags()

    def commands(self):
        """
        get a list of the commands inside the email

        Everithing with the form [[cmd|params]] will be reconice as command

        @returns: [(cmd, params)]
        """
        comexp = re.compile(r"\[\[([^\|]*)\|([^\]]*)\]\]")
        text = self._['Body']
        return comexp.findall(text)

    def tags(self):
        """
        get a list of the tags from the subject

        The text between [ and ] is consider as a tag

        @returns: [tag]
        """
        tagexp = re.compile(r"\[([^\]]*)\]")
        subject = self._['Subject']
        return tagexp.findall(subject)


def _msg_to_dict(msg):
    # FIXME: any repeated header will be ignored
    # Usually it is only 'Received' header
    d = {}
    for header in msg.keys():
        d[header] = msg.get_decoded_header(header)
    body = msg.text_part.get_payload()
    d['Body'] = body.decode(msg.text_part.charset).encode('UTF-8')

    attach = []
    for mailpart in msg.mailparts:
        a = dict(mailpart.part)
        body = mailpart.get_payload()
        if mailpart.charset:
            body.decode(mailpart.charset).encode('UTF-8')
        a['Body'] = body
        attach.append(a)
    d['Attachments'] = attach

    return d
