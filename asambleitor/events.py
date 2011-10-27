_events = {}

def trigger(event, data):
    if event not in _events:
        return
    for handler in _events[event]:
        handler(event, data)

def subscribe(event, handler):
    if event in _events:
        _events[event].append(handler)
    else:
        _events[event] = [handler]

def unsubscribe(event, handler):
    _events[event].remove(handler)
