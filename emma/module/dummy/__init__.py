from emma.events import subscribe
from emma.module import module

class dummy(module):
    def run(self):
        subscribe(self.handler_rcv, 'receive', 'email')
        subscribe(self.handler_cmd, 'command')

    def handler_rcv(self, event, producer, message):
        print message['subject']
        print message.get_payload()

    def handler_cmd(self, event, producer, command):
        if command[0] == "print":
            print command[1]
