import json

from modcore import modc, Module, LifeCycle
from modcore.log import LogSupport, logger
from modext.config import ReprDict, Namespace, ensure_path

from .settings import mod_settings


class BaseContainer(ReprDict):
    def move(self, pos, d):
        # requires self.el
        t = self.el.pop(pos)
        self.el.insert(pos + d, t)

    def add(self, el):
        self.el.append(el)

    def remove(self, pos):
        self.el.pop(pos)


class Task(BaseContainer):
    def __init__(self, valves):
        self.el = valves

    def __repr__(self):
        return self.el


class Program(BaseContainer, LogSupport):
    def __init__(self, id, name, active, tasklist):
        LogSupport.__init__(self)
        self.id = id
        self.name = name
        self.active = active
        self.el = tasklist

    def get_tasks(self):
        return self.el

    def __repr__(self):
        return {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "tasks": self.get_tasks(),
        }


FNAM = "/etc/" + mod_settings.app + "/programs.json.txt"


class Programs(BaseContainer, LogSupport):
    def __init__(self, programlist):
        LogSupport.__init__(self)
        self.el = programlist
        self.save_cb = None

    def __repr__(self):
        return self.reprlist(self.el)

    def create(self, progs):
        pl = list(map(lambda x: Program(x.id, x.name, x.active, x.tasks), progs))
        return pl

    def load(self):
        try:
            with open(FNAM, "r") as f:
                cont = f.read()
                progs = list(map(lambda x: Namespace().update(x), json.loads(cont)))
                self.info("loaded", progs)
                self.el = self.create(progs)
        except Exception as ex:
            self.excep(ex, "json failed")

        return self

    def save(self, progs):
        self.el = self.create(progs)
        if self.save_cb != None:
            self.save_cb()
        ensure_path(FNAM)
        with open(FNAM, "w") as f:
            jslist = self.reprlist(self.el)
            cont = json.dumps(jslist)
            f.write(cont)
        return self

    def get_program(self, pos):
        return self.el[pos]

    def get_program_list(self):
        return self.el

    def get_programs(self):
        return self.reprlist(self.el)

    def get_program_by_id(self, progid):
        return list(filter(lambda x: x.id == progid, self.get_program_list()))[0]


def reload_programs():
    logger.info("reload_programs")
    return Programs([]).load()


mod_programs = reload_programs()
