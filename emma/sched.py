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
from cPickle import dumps
from time import strptime, mktime

from events import trigger
from database import DB


def str2date(date):
    """
    Convert an string of date to a epoch date

    @type date: string
    @param date: string date of the date
    @returns: epoch date
    """
    date_fmt = [_("%d/%m/%Y %H:%M"), _("%d/%m/%Y")]

    for fmt in date_fmt:
        try:
            return mktime(strptime(date, fmt))
        except ValueError:
            pass
    return -1


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


def at(event, data, date, doc_id=None):
    """
    Program an event to be trigger on a date

    @type event: Event
    @param event: event to be scheduled
    @param data: data for the event
    @type date: int or string
    @param date: epoch date or string date for the event
    @type doc_id: ObjectId
    @param doc_id: optional database document id where is stored the scheduled
    event. Meant to be use on recovering sched from the database, like after
    a shutdown
    """
    epoch = -1
    if isinstance(date, int):
        epoch = date
    elif isinstance(date, str):
        epoch = str2date(date)

    if epoch != -1:
        args = (event, data, epoch - time(), epoch, doc_id)
        thread.start_new_thread(_delay, args)
    return epoch


def delay(event, data, seconds, doc_id=None):
    """
    Program an event to be trigger after some seconds

    @type event: Event
    @param event: event to be scheduled
    @param data: data for the event
    @type seconds: int
    @param seconds: seconds of delay for the event
    @type doc_id: ObjectId
    @param doc_id: optional database document id where is stored the scheduled
    event. Meant to be use on recovering sched from the database, like after
    a shutdown
    @warning: it is not properly tested might have bugs
    """
    thread.start_new_thread(_delay, (event, data, seconds, seconds + time()))


def _delay(event, data, seconds, date, doc_id=None):
    db = DB()
    core = db.core()
    if not doc_id:
        doc = {'element': 'sched',
            'type': 'at',
            'event': dumps(event.elements()),
            'data': dumps(data),
            'date': date}
        doc_id = core.insert(doc)

    if seconds > 0:
        sleep(float(seconds))
    trigger(event, data)
    core.remove(doc_id)
