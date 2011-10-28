from email.feedparser import FeedParser

def parse(email):
    p = FeedParser()
    for line in email:
        p.feed(line)
    return p.close()
