from emma.log import log

class Complement:
    def __init__(self, identifier, conf):
        self.conf = conf
        self.identifier = identifier

    def run(self):
        pass

    def log(self, msg):
        name = self.__module__.split(".")[-1]
        log("[" + name + " " + self.identifier + "] " + msg)
