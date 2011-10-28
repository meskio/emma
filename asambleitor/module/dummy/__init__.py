from asambleitor.events import subscribe
from asambleitor.module import module

class dummy(module):
    def run(self):
        subscribe(self.handler, 'receive', 'email')

    def handler(self, event, producer, data):
        print data['subject']
        print data.get_payload()
