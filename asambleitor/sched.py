import thread
from time import sleep, time

from asambleitor.events import trigger

def periodic(event, data, seconds):
    thread.start_new_thread(_periodic, (event, data, seconds))

def _periodic(event, data, seconds):
    while 1:
        sleep(seconds)
        trigger(event, data)

def at(event, data, date):
    thread.start_new_thread(_delay, (event, data, date - time()))

def delay(event, data, seconds):
    thread.start_new_thread(_delay, (event, data, seconds))

def _delay(event, data, seconds):
    sleep(seconds)
    trigger(event, data)
