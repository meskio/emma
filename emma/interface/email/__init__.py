import poplib

from emma.interface import interface
from emma.sched import periodic
from emma.events import trigger
from emma.log import log

from parser import Parser


class email(interface):
    def run(self):
        period = self.conf['pop_period']
        periodic(self.fetch, period)

    def fetch(self):
        log("[email] fetching email " + self.conf['pop_user']
                + "@" + self.conf['pop_host'])

        try:
            if self.conf['pop_ssl'] == "yes":
                pop = poplib.POP3_SSL(self.conf['pop_host'])
            else:
                pop = poplib.POP3(self.conf['pop_host'])
            pop.user(self.conf['pop_user'])
            pop.pass_(self.conf['pop_pass'])
        except:
            log("[email]     error connecting by POP3")
            return

        numMessages = len(pop.list()[1])
        for i in range(numMessages):
            p = Parser(pop.retr(i+1)[1])
            message = p.message()
            trigger('receive', 'email', message)
            for command in p.commands():
                trigger('command', 'email', command)
            pop.dele(i+1)

        pop.quit()
        log("[email]     " + str(numMessages) + " found")
