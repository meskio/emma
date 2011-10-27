import thread

from asambleitor.sched import periodic
from asambleitor.interface import interface


class email(interface):
    def run(self):
        periodic('print', self.conf['str'], 1)
