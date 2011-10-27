from time import sleep
import thread

from asambleitor.events import trigger
from asambleitor.interface import interface


class email(interface):
    def __init__(self, conf):
        interface.__init__(self, conf)
        thread.start_new(self.push, ())

    def push(self):
        sleep(1)
        trigger('print', self.conf['str'])
