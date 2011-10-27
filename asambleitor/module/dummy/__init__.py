from asambleitor.events import subscribe,unsubscribe
from asambleitor.module import module

class dummy(module):
    def __init__(self, conf):
        module.__init__(self, conf)
        subscribe('foo', self.handler)

    def handler(self, event, data):
        print "hola mundo"
        unsubscribe(event, self.handler)
