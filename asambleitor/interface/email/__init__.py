from time import sleep
import thread
from asambleitor.events import trigger

def push():
    sleep(1)
    trigger('foo',None)

def init(conf):
    thread.start_new(push, ())
    
