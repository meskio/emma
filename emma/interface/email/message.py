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

        d = msg_to_dict(msg)
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


def msg_to_dict(msg):
    """
    Convert a PyZmail message to a dictionary

    @type msg: PyzMessage
    @param msg: email to convert
    @returns: {'Header': 'content'}
    """
    # FIXME: any repeated header will be ignored
    # Usually it is only 'Received' header
    d = {}

    if msg.text_part:
        body = msg.text_part.get_payload()
        charset = msg.text_part.charset
    else:
        body = msg.get_payload()
        charset = msg.get_charset()
    if charset:
        charset = charset.lower()
        i = charset.find('iso')
        u = charset.find('utf')
        if i > 0:
            charset = charset[i:]
        elif u > 0:
            charset = charset[u:]
        # Some old emails say it's ascii or unkown but in reality is not
        # not use any charset not iso or utf
        elif i != 0 and u != 0:
            charset = None

    for header in msg.keys():
        value = msg.get_decoded_header(header)
        value, _ = pyzmail.decode_text(value, charset, None)
        value = value.encode('UTF-8')
        header = header.replace('.',',') # mongoDB don't likes '.' on keys
        d[header] = value

    attach = []
    if type(body) == str:
        body, _ = pyzmail.decode_text(body, charset, None)
        body = body.encode('UTF-8')
    # On attachments of emails sometimes it end up with a list of email.message
    elif type(body) == list:
        for part in body:
            zmail = pyzmail.PyzMessage(part)
            a = msg_to_dict(zmail)
            attach.append(a)
        body = attach[0]['Body']
    d['Body'] = body

    if len(msg.mailparts) > 1:
        for mailpart in msg.mailparts:
            zmail = pyzmail.PyzMessage(mailpart.part)
            a = msg_to_dict(zmail)
            attach.append(a)

    if attach:
        d['Attachments'] = attach

    return d
