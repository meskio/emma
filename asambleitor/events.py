events = {}

def trigger(event, data):
    if event not in events:
        return
    for handler in events[event]:
        handler(event, data)

def subscribe(event, handler):
    if event in events:
        events[event].append(handler)
    else:
        events[event] = [handler]

def unsubscribe(event, handler):
    events[event].remove(handler)
