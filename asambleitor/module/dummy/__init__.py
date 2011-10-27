from asambleitor.events import subscribe,unsubscribe

def h(event, data):
    print "hola mundo"
    unsubscribe(event, h)

def init(conf):
    subscribe('foo', h)
