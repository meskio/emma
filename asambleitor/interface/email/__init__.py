from time import sleep
import thread

from asambleitor.sched import periodic
from asambleitor.interface import interface


class email(interface):
    def __init__(self, conf):
        interface.__init__(self, conf)
        periodic('print', self.conf['str'], 1)
