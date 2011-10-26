import ConfigParser

def init(confPath):
    conf = ConfigParser.RawConfigParser()
    conf.read(confPath)

    for s in conf.sections():
        options = dict(conf.items(s))

        if s[0] == 'M':
            name = s[2:-2]
            module = __import__("module."+name)
            exec "module." + name + ".init(options)"
        if s[0] == 'I':
            name = s[2:-2]
            interface = __import__("interface."+name)
            exec "interface." + name + ".init(options)"
