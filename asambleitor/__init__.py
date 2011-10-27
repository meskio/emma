import thread
import ConfigParser
from time import sleep

confPath = '/usr/local/etc/asambleitor.cfg'

def main():
    conf = ConfigParser.RawConfigParser()
    conf.read(confPath)

    for section in conf.sections():
        options = dict(conf.items(section))

        name = section[2:-2]
        if section[0] == 'M':
            imp = __import__("asambleitor.module." + name)
            exec "m = imp.module." + name + "." + name + "(options)"
            thread.start_new_thread(m.run, ())
        if section[0] == 'I':
            imp = __import__("asambleitor.interface." + name)
            exec "i = imp.interface." + name + "." + name + "(options)"
            thread.start_new_thread(i.run, ())

    while 1: sleep(1000)
