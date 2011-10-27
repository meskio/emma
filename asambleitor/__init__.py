from time import sleep
import ConfigParser

confPath = '/usr/local/etc/asambleitor.cfg'

def main():
    conf = ConfigParser.RawConfigParser()
    conf.read(confPath)

    for section in conf.sections():
        options = dict(conf.items(section))

        name = section[2:-2]
        if section[0] == 'M':
            m = __import__("asambleitor.module." + name)
            exec "m.module." + name + "." + name + "(options)"
        if section[0] == 'I':
            m = __import__("asambleitor.interface." + name)
            exec "m.interface." + name + "." + name + "(options)"

    sleep(2)
