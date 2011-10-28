import thread

_events = {}
_events_lock = thread.allocate_lock()

def trigger(event, data):
    if event not in _events:
        return
    for handler in _events[event]:
        thread.start_new_thread(handler, (event, data))

def subscribe(event, handler):
    _events_lock.acquire()
    if event in _events:
        _events[event].append(handler)
    else:
        _events[event] = [handler]
    _events_lock.release()

def unsubscribe(event, handler):
    with _events_lock:
        _events[event].remove(handler)
