from asambleitor.events import subscribe,unsubscribe
from asambleitor.module import module

class dummy(module):
    def run(self):
        subscribe('print', self.handler)

    def handler(self, event, data):
        print data
        #unsubscribe(event, self.handler)
