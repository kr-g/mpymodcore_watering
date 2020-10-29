import json

from modcore import modc, Module, LifeCycle
from modcore.log import LogSupport, logger
from modext.config import ReprDict, Namespace, ensure_path

from .settings import mod_settings


class Schedule(ReprDict, LogSupport):
    def __init__(self, id, name, program, time, dow, active):
        LogSupport.__init__(self)
        self.id = id
        self.name = name
        self.program = program
        self.time = time
        self.dow = dow
        self.active = active

    def __repr__(self):
        return {
            "id": self.id,
            "name": self.name,
            "program": self.program,
            "time": self.time,
            "dow": self.dow,
            "active": self.active,
        }


FNAM = "/etc/" + mod_settings.app + "/scheduled.json.txt"


class Scheduled(ReprDict, LogSupport):
    def __init__(self, scheduled):
        LogSupport.__init__(self)
        self.el = scheduled
        self.save_cb = None

    def __repr__(self):
        return self.reprlist(self.get_schedule())

    def create(self, scheduled):
        pl = list(
            map(
                lambda x: Schedule(x.id, x.name, x.program, x.time, x.dow, x.active),
                scheduled,
            )
        )
        return pl

    def load(self):
        try:
            with open(FNAM, "r") as f:
                cont = f.read()
                scheduled = list(map(lambda x: Namespace().update(x), json.loads(cont)))
                self.info("loaded", scheduled)
                self.el = self.create(scheduled)
        except Exception as ex:
            self.excep(ex, "json failed")

        return self

    def save(self, scheduled):
        self.el = self.create(scheduled)
        if self.save_cb != None:
            self.save_cb()
        ensure_path(FNAM)
        with open(FNAM, "w") as f:
            jslist = self.reprlist(self.el)
            cont = json.dumps(jslist)
            f.write(cont)
        return self

    def get_scheduled(self):
        return self.reprlist(self.el)

    def get_schedule(self):
        return self.el


def reload_schedule():
    logger.info("reload_schedule")
    return Scheduled([]).load()


mod_scheduled = reload_schedule()
