import emma.events
from emma.events import *

from test.monkey import *


class TestEvent:
    e1 = Event(event="db", interface="xmpp", identifier="emma")
    e2 = Event(event="db", identifier="emma")

    def test_event(self):
        assert self.e1.event == "db"

    def test_interface(self):
        assert self.e1.interface == "xmpp"

    def test_identifier(self):
        assert self.e1.identifier == "emma"

    def test_init(self):
        assert self.e1.event == "db"
        assert self.e1.interface == "xmpp"
        assert self.e1.identifier == "emma"

    def test_half_init(self):
        assert self.e2.event == "db"
        assert self.e2.interface == None
        assert self.e2.identifier == "emma"

    def test_elemnts(self):
        assert self.e1.elements() == ("db", "xmpp", "emma")
        assert self.e2.elements() == ("db", None, "emma")

    def test_gen_events(self):
        assert self.e1.all_events() == set([Event('db', 'xmpp', None),
                                            Event(None, None, 'emma'),
                                            Event('db', None, 'emma'),
                                            Event(None, 'xmpp', None),
                                            Event(None, None, None),
                                            Event('db', 'xmpp', 'emma'),
                                            Event('db', None, None),
                                            Event(None, 'xmpp', 'emma')])
        assert self.e2.all_events() == set([Event('db', None, None),
                                            Event(None, None, None),
                                            Event(None, None, 'emma'),
                                            Event("db", None, 'emma')])

    def test_cmp(self):
        event = Event(event="db", interface="xmpp", identifier="emma")
        assert event == self.e1
        assert event != self.e2

    def test_hash(self):
        event = Event(event="db", interface="xmpp", identifier="emma")
        assert event.__hash__() == self.e1.__hash__()
        assert event.__hash__() != self.e2.__hash__()


# mock the _events dictionary
def myEvents(monkeypatch, events):
    monkeypatch.setattr(emma.events, '_events', events)


def test_trigger_dummy(monkeypatch):
    myThread = MyThread(monkeypatch)
    def handler(event, data):
        return "foo"
    myEvents(monkeypatch, {Event("foo"): [handler]})
    trigger(Event("foo", "irc", "emma"), None)
    assert myThread.result[0] == "foo"


def test_trigger_get_data(monkeypatch):
    myThread = MyThread(monkeypatch)
    def handler(event, data):
        return data
    myEvents(monkeypatch, {Event("foo"): [handler]})
    trigger(Event("foo", "irc", "emma"), 12)
    assert myThread.result[0] == 12


def test_trigger_multy_subscriptions(monkeypatch):
    myThread = MyThread(monkeypatch)
    def h1(event, data):
        return data
    def h2(event, data):
        return data + 2
    myEvents(monkeypatch, {Event("foo"): [h1],
                           Event(interface="irc", identifier="emma"): [h2]})
    trigger(Event("foo", "irc", "emma"), 12)
    assert set(myThread.result) == set([12, 14])


def test_run_event_get_data(monkeypatch):
    myThread = MyThread(monkeypatch)
    def h1(event, data):
        return data
    def h2(event, data):
        return data + 2
    myEvents(monkeypatch, {Event("foo"): [h1],
                           Event(interface="irc", identifier="emma"): [h2]})
    result = run_event(Event("foo", "irc", "emma"), 12)
    assert set(result) == set([12, 14])


def test_subscribe_handler(monkeypatch):
    events = {}
    myEvents(monkeypatch, events)
    def handler(event, data):
        pass
    subscribe(Event("foo"), handler)
    assert events[Event("foo")] == [handler]


def test_subscribe_existing_events(monkeypatch):
    def h1(event, data):
        pass
    def h2(event, data):
        pass
    events = {Event("foo"): [h1]}
    myEvents(monkeypatch, events)
    subscribe(Event("foo"), h2)
    assert events[Event("foo")] == [h1,h2]


def test_unsubscribe_handler(monkeypatch):
    def h1(event, data):
        pass
    events = {Event("foo"): [h1]}
    myEvents(monkeypatch, events)
    unsubscribe(Event("foo"), h1)
    assert events[Event("foo")] == []


def test_unsubscribe_existing_events(monkeypatch):
    def h1(event, data):
        pass
    def h2(event, data):
        pass
    events = {Event("foo"): [h1,h2]}
    myEvents(monkeypatch, events)
    unsubscribe(Event("foo"), h2)
    assert events[Event("foo")] == [h1]


def test_unsubscribe_nonexist(monkeypatch):
    def h1(event, data):
        pass
    myLogger = MyLogging(monkeypatch)
    events = {}
    myEvents(monkeypatch, events)
    unsubscribe(Event("foo"), h1)
    assert myLogger.log
