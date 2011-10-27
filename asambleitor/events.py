events = {}

def subscribe(event, handler):
    if event in events:
        events[event].append(handler)
    else:
        events[event] = [handler]

def trigger(event, data):
    if event not in events:
        return
    for handler in events[event]:
        handler(data)
