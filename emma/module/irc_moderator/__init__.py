import thread

from emma.events import Event, subscribe, trigger
from emma.module import Module

class irc_moderator(Module):
    def run(self):
        self.lock = thread.allocate_lock()
        self.on_moderate = False

        cmd_event = Event(event="command", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(cmd_event, self.cmd_handler)
        rcv_event = Event(event="receive", interface="irc", \
                          identifier=self.conf['irc_id'])
        subscribe(rcv_event, self.rcv_handler)

    def cmd_handler(self, event, data):
        self.lock.acquire()
        cmd, args = data[0]
        if cmd == "moderate" and not self.on_moderate:
            self.log("Start moderating")
            self.on_moderate = True
            self.words = []
            self.talking = None
        elif cmd == "stop":
            self.log("Stop moderating")
            self.on_moderate = False
        elif cmd == "word":
            nick = data[1]['from']
            self.log("Request word from: " + nick)
            if self.talking:
                self.words.append(nick)
            else:
                self.talking = nick
                self.give_turn(nick)
        self.lock.release()

    def rcv_handler(self, event, data):
        self.lock.acquire()
        if self.on_moderate:
            if data['body'] == "." and data['from'] == self.talking:
                if self.words:
                    self.talking = self.words[0]
                    self.words = self.words[1:]
                    self.give_turn(self.talking)
                else:
                    self.talking = None
        self.lock.release()

    def give_turn(self, nick):
        self.log("Give word to: " + nick)
        msg = nick + " has the word"
        event = Event(event="send", interface="irc", \
                      identifier=self.conf['irc_id'])
        trigger(event, (self.conf['irc_chn'], msg))
