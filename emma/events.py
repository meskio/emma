"""
Event support for emma

The events are addressed by L{Event} class, with the event name, interface and
identifier of the L{interface} related to it. Any complement can be scubcribed
and trigger any event.

@copyright: (c) 2011 hackmeeting U{http://sindominio.net/hackmeeting}
@author: Ruben Pollan
@organization: hackmeeting U{http://sindominio.net/hackmeeting}
@contact: meskio@sindominio.net
@license:
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  U{http://sam.zoy.org/projects/COPYING.WTFPL} for more details.
"""

import thread
import itertools

class Event:
    """
    Event addressing class

    It holds the event name, interface and identifier of the event. You can
    access to each of them from the object once instanciated:

    >>> myEvent = Event(event="foo", identifier="bar")
    >>> myEvent.event
    'foo'
    >>> myEvent.interface
    >>> myEvent.identifier
    'bar'
    """
    def __init__(self, event=None, interface=None, identifier=None):
        """
        Define the event

        Set the event name, interface and identifier, none of them is required.
        Any of the three elements empty will mean that the event subscription
        will get all the events with the element or elements defined.

        @type event: string
        @param event: name of the event
        @type interface: string
        @param interface: interface producer or receiver of the event
        @type identifier: string
        @param identifier: the identifier string of the interface
        """
        self.event = event
        self.interface = interface
        self.identifier = identifier

    def __cmp__(self, event):
        return cmp(self.elements(), event.elements())

    def __hash__(self):
        return self.elements().__hash__()

    def elements(self):
        """
        Get the elements of the event

        @returns: (event, interface, identifier)
        """
        return (self.event, self.interface, self.identifier)

    def all_events(self):
        """
        Get all the events that will be trigger with it

        @returns: [all the combinations of None and elements of the event]
        @attention: this method is meant to be use only inside L{emma.events}
        """
        event_tuples = itertools.product((self.event, None), \
                                         (self.interface, None), \
                                         (self.identifier, None))
        events = [ Event(x,y,z) for x,y,z in event_tuples]
        return events


_events = {}
_events_lock = thread.allocate_lock()

def _get_handlers(event):
    handlers = []
    for e in event.all_events():
        if e in _events:
            handlers += _events[e]
    return set(handlers)

def trigger(event, data):
    """
    Trigger an event on background

    Execute in a new thread each handler L{subscribe}d to the event.

    @type event: L{Event}
    @param event: event to be triggered, it must have all the elements
    @type data: undefined
    @param data: the information passed by the event, each event will define
    it's data structure
    @warning: event can not have any None value
    """
    handlers = _get_handlers(event)

    for handler in handlers:
        thread.start_new_thread(handler, (event, data))

def run_event(event, data):
    """
    Run an event waiting for it's result

    Execute each handler L{subscribe}d to the event secuentially getting back
    the return value of each handler.

    @type event: L{Event}
    @param event: event to be triggered, it must have all the elements
    @type data: undefined
    @param data: the information passed by the event, each event will define
    it's data structure
    @returns: [return value of each event handler]
    @warning: event can not have any None value
    """
    handlers = _get_handlers(event)

    res = []
    for handler in handlers:
        res.append(handler(event, data))
    return res

def subscribe(event, handler):
    """
    Subscribe to an event

    Set a function to be call if an event is produced. The event can have some
    (or all) elements undefined, so it was call by any event with the defined
    elements equals to the subscribed event.

    @type event: L{Event}
    @param event: event to be triggered
    @type handler: fun(event, data)
    @param handler: function to call if the event is trigger
    """
    _events_lock.acquire()
    if event not in _events:
        _events[event] = [handler]
    else:
        _events[event].append(handler)
    _events_lock.release()

def unsubscribe(event, handler):
    """
    Unsubscribe from an event

    @type event: L{Event}
    @param event: event used for subscription
    @type handler: fun(event, data)
    @param handler: the function used for subscription
    @warning: it is not properly tested might have bugs
    """
    with _events_lock:
        if event in _events:
            _events[event].remove(handler)
        else:
            log("[core] can't unsubscribe identifier, it was not subscribed")
