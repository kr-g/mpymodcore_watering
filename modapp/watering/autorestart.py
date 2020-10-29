import json

from modcore import modc

from moddev.alarmclock import AlarmClock
from modext.config import ReprDict


FNAM = "autoreboot.cfg.txt"


class AutoRestart(AlarmClock, ReprDict):
    def conf(self, config=None):
        cfg = {
            self.id: self.autorestart,
            self.id + ":event": "restart:hard",
        }
        super().conf(cfg)

    def load(self):
        self.info("load")
        # called before modc.start
        self.autorestart = None
        try:
            with open(FNAM, "r") as f:
                cont = f.read()
                self.autorestart = cont if len(cont) > 0 else None
        except:
            pass
        return self

    def save(self, autorestart="23:59"):
        self.info("save")
        self.autorestart = autorestart

        self.conf()
        self.recalc()

        with open(FNAM, "w") as f:
            if self.autorestart != None and len(self.autorestart) > 0:
                f.write(self.autorestart)
        return self

    def get_autorestart(self):
        return self.autorestart


mod_autorestart = AutoRestart("autorestart").load()
modc.add(mod_autorestart)
