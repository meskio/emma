import thread
import random
from time import sleep, time

from asambleitor.events import trigger


def periodic(handler, seconds):
    #event = 'periodic_' + str(random.randrange(0, 100000))
    #subscribe(event, handler)
    thread.start_new_thread(_periodic, (handler, seconds))

def _periodic(handler, seconds):
    while 1:
        sleep(float(seconds))
        handler()

def at(event, data, date):
    thread.start_new_thread(_delay, (event, data, date - time()))

def delay(event, data, seconds):
    thread.start_new_thread(_delay, (event, data, seconds))

def _delay(event, data, seconds):
    sleep(float(seconds))
    trigger(event, data)
