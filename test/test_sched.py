import emma.sched
from emma.sched import *

from emma.events import Event
from test.monkey import *
from cPickle import dumps


def test_delay(monkeypatch):
    myThread = MyThread(monkeypatch)
    myEvents = MyEvents(monkeypatch, emma.sched)
    myDB = MyDB(monkeypatch, emma.sched)
    delay(Event(), None, 0)
    assert myEvents.event == Event()


def test_delay_store(monkeypatch):
    myThread = MyThread(monkeypatch)
    myEvents = MyEvents(monkeypatch, emma.sched)
    myDB = MyDB(monkeypatch, emma.sched)
    delay(Event(), None, 0)
    data = myDB.deleted[0]
    assert data['element'] == "sched"
    assert data['type'] == "at"
    assert data['data'] == dumps(None)
