from asambleitor.events import subscribe
from asambleitor.module import module

class dummy(module):
    def run(self):
        subscribe('recv_email', self.handler)

    def handler(self, event, data):
        print data['subject']
        print data.get_payload()
