import thread

from emma.log import log

def use_lock(fn):
    def wrapper(self, *arg):
        self.lock.acquire()
        res = fn(self, *arg)
        self.lock.release()
        return res
    return wrapper

class Complement:
    def __init__(self, identifier, conf):
        self.conf = conf
        self.identifier = identifier
        self.lock = thread.allocate_lock()

    def run(self):
        pass

    def log(self, msg):
        name = self.__module__.split(".")[-1]
        log("[" + name + " " + self.identifier + "] " + msg)
