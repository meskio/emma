from asambleitor.events import subscribe

def h(data):
    print "hola mundo"

def init(conf):
    subscribe('foo', h)
