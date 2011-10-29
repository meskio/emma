import thread
import ConfigParser
import re
from time import sleep

from log import log

confPath = '/usr/local/etc/emma.cfg'

def main():
    conf = ConfigParser.RawConfigParser()
    conf.read(confPath)
    log.activate = conf.getboolean("core", "log")

    log("[core] preparing interfaces and modules")
    sectexp = re.compile(r"^[IM] ([^ ]*) (.*)$")
    for section in conf.sections():
        options = dict(conf.items(section))

        m = sectexp.match(section)
        if not m:
            continue
        name, identifier = m.groups()
        if section[0] == 'M':
            log("[core]     load module " + name)
            imp = __import__("emma.module." + name)
            exec "m = imp.module." + name + "." + name \
                    + "('" + identifier + "', options)"
            thread.start_new_thread(m.run, ())
        if section[0] == 'I':
            log("[core]     load interface " + name)
            imp = __import__("emma.interface." + name)
            exec "i = imp.interface." + name + "." + name \
                    + "('" + identifier + "', options)"
            thread.start_new_thread(i.run, ())

    while 1: sleep(1000)
