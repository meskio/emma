import thread

_events = {}
_events_lock = thread.allocate_lock()

def trigger(event, producer, data):
    if event not in _events:
        return
    if producer in _events[event]:
        for handler in _events[event][producer]:
            thread.start_new_thread(handler, (event, producer, data))
    if None in _events[event]:
        for handler in _events[event][None]:
            thread.start_new_thread(handler, (event, producer, data))

def subscribe(handler, event, producer=None):
    _events_lock.acquire()
    if event not in _events:
        _events[event] = {producer: [handler]}
    elif producer not in _events[event]:
        _events[event][producer] = [handler]
    else:
        _events[event][producer].append(handler)
    _events_lock.release()

def unsubscribe(handler, event, producer=None):
    with _events_lock:
        if event in _events and producer in _events[event]:
            _events[event][producer].remove(handler)
