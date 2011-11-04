from email.feedparser import FeedParser
import email.message
import re

class Message:
    def __init__(self, list_lines):
        p = FeedParser()
        for line in list_lines:
            p.feed(line + "\n")
        self.message = p.close()

        self.lines = list_lines
        self.comexp = re.compile(r"\[\[([^\|]*)\|([^\]]*)\]\]")
        self.tagexp = re.compile(r"\[([^\]]*)\]")

    def __getitem__(self, item):
        if item == 'body':
            return self.message.get_payload()
        elif item == 'commands':
            return self.commands()
        elif item == 'tags':
            return self.tags()
        elif item == 'type':
            return "email"
        elif item in self.message:
            return self.message[item]
        else:
            return ""

    def commands(self):
        text = self['body']
        return self.comexp.findall(text)

    def tags(self):
        return self.tagexp.findall(self['subject'])
