import thread
import itertools

class Event:
    def __init__(self, event=None, interface=None, identifier=None): 
        self.event = event
        self.interface = interface
        self.identifier = identifier

    def __cmp__(self, event):
        return cmp(self.elements(), event.elements())

    def __hash__(self):
        return self.elements().__hash__()

    def elements(self):
        return (self.event, self.interface, self.identifier)

    def all_events(self):
        event_tuples = itertools.product((self.event, None), \
                                         (self.interface, None), \
                                         (self.identifier, None))
        events = [ Event(e[0], e[1], e[2]) for e in event_tuples]
        return events


_events = {}
_events_lock = thread.allocate_lock()

def trigger(event, data):
    #FIXME: event can not have any None value
    h = []
    for e in event.all_events():
        if e in _events:
            h += _events[e]
    handlers = set(h)

    for handler in handlers:
        thread.start_new_thread(handler, (event, data))

def subscribe(event, handler):
    _events_lock.acquire()
    if event not in _events:
        _events[event] = [handler]
    else:
        _events[event].append(handler)
    _events_lock.release()

def unsubscribe(event, handler):
    with _events_lock:
        if event in _events:
            _events[event].remove(handler)
        else:
            log("[core] can't unsubscribe identifier, it was not subscribed")
