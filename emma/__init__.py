import thread
import ConfigParser
from time import sleep

from log import log

confPath = '/usr/local/etc/emma.cfg'

def main():
    conf = ConfigParser.RawConfigParser()
    conf.read(confPath)
    log.activate = conf.getboolean("core", "log")

    log("[core] preparing interfaces and modules")
    for section in conf.sections():
        options = dict(conf.items(section))

        name = section[2:-2]
        if section[0] == 'M':
            log("[core]     load module " + name)
            imp = __import__("emma.module." + name)
            exec "m = imp.module." + name + "." + name + "(options)"
            thread.start_new_thread(m.run, ())
        if section[0] == 'I':
            log("[core]     load interface " + name)
            imp = __import__("emma.interface." + name)
            exec "i = imp.interface." + name + "." + name + "(options)"
            thread.start_new_thread(i.run, ())

    while 1: sleep(1000)
