import thread
import random
from time import sleep, time

from events import trigger


def periodic(handler, seconds):
    thread.start_new_thread(_periodic, (handler, seconds))

def _periodic(handler, seconds):
    while 1:
        handler()
        sleep(float(seconds))

def at(event, data, date):
    thread.start_new_thread(_delay, (event, data, date - time()))

def delay(event, data, seconds):
    thread.start_new_thread(_delay, (event, data, seconds))

def _delay(event, data, seconds):
    sleep(float(seconds))
    trigger(event, data)
