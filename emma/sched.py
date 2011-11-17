"""
Schedule actions or events

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
import random
from time import sleep, time

from events import trigger


def periodic(handler, seconds):
    """
    Program a periodic action

    Execute I{handler} each I{seconds} in parallel.

    @type handler: fun()
    @param handler: function to call each I{seconds}
    @type seconds: integer
    @param seconds: waiting seconds between the end of a handler call and the
    next
    """
    thread.start_new_thread(_periodic, (handler, seconds))

def _periodic(handler, seconds):
    while 1:
        handler()
        sleep(float(seconds))

def at(event, data, date):
    """
    Program an event to be trigger on a date

    @warning: the syntax might change
    @warning: it is not properly tested might have bugs
    """
    thread.start_new_thread(_delay, (event, data, date - time()))

def delay(event, data, seconds):
    """
    Program an event to be trigger after some seconds

    @warning: the syntax might change
    @warning: it is not properly tested might have bugs
    """
    thread.start_new_thread(_delay, (event, data, seconds))

def _delay(event, data, seconds):
    sleep(float(seconds))
    trigger(event, data)
