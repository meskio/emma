import poplib
import smtplib

from emma.interface import interface
from emma.sched import periodic
from emma.events import trigger, subscribe
from emma.log import log

from parser import Parser


class email(interface):
    def run(self):
        period = self.conf['pop_period']
        periodic(self.fetch, period)
        subscribe(self.send_handle, 'send_'+self.conf['id'])

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

    def send_handle(self, event, provider, msg):
        msg['From'] = self.conf['smtp_address']
        self.send(msg['To'], msg.as_string())

    def send(self, to, msg):
        try:
            if self.conf['smtp_ssl'] == "yes":
                server = smtplib.SMTP_SSL(self.conf['smtp_host'])
            else:
                server = smtplib.SMTP(self.conf['smtp_host'])
            #server.set_debuglevel(1)
            if self.conf['smtp_tls'] == "yes":
                server.starttls()
            server.login(self.conf['smtp_user'], self.conf['smtp_pass'])
        except:
            log("[email]     error sending email")
            return

        fromaddr = self.conf['smtp_address']
        server.sendmail(fromaddr, to, msg)
        server.quit()
