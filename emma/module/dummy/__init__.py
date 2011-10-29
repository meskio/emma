from email.mime.text import MIMEText

from emma.events import Event, subscribe, trigger
from emma.module import Module

class dummy(Module):
    def run(self):
        recv_event = Event(event='receive', interface='email')
        subscribe(recv_event, self.handler_rcv)
        cmd_event = Event(event='command')
        subscribe(cmd_event, self.handler_cmd)

    def handler_rcv(self, event, message):
        print message['subject']
        print message.get_payload()

    def handler_cmd(self, event, command):
        if command[0] == "print":
            print command[1]
        if command[0] == "send":
            msg = MIMEText(command[1])
            msg['Subject'] = "from emma bot"
            msg['To'] = self.conf['send_to']
            send_event = Event(event='send', interface='email', identifier=self.conf['send_id'])
            trigger(send_event, msg)
