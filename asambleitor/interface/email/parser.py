from email.feedparser import FeedParser
import re

class Parser:
    def __init__(self, list_lines):
        self.comexp = re.compile(r"\[\[([^\|]*)\|([^\]]*)\]\]")

        self.lines = list_lines
        p = FeedParser()
        for line in list_lines:
            p.feed(line + "\n")
        self._message = p.close()

    def message(self):
        return self._message

    def commands(self):
        text = self._message.get_payload()
        return self.comexp.findall(text)
