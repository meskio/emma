import thread
import logging


# mock the gettext _(...) function
import __builtin__
__builtin__.__dict__['_'] = lambda msg: msg


class MyThread:
    def __init__(self, monkeypatch):
        self.result = []
        monkeypatch.setattr(thread, 'start_new_thread', self.start)

    def start(self, handler, args):
        self.result.append(handler(*args))


class MyLogging:
    def __init__(self, monkeypatch):
        self.log = False
        self.text = ""
        self.level = None

        monkeypatch.setattr(logging, 'log', self.handler)
        levels = (logging.CRITICAL, logging.ERROR, logging.WARNING,
                  logging.INFO, logging.DEBUG)
        for level in levels:
            name = logging.getLevelName(level).lower()
            h = lambda msg: self.handler(msg, level)
            monkeypatch.setattr(logging, name, h)

    def handler(self, msg, level):
        self.log = True
        self.text = msg
        self.level = level
