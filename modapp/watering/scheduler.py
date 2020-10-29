from machine import Pin

from modcore import modc, Module, LifeCycle
from modcore.log import LogSupport
from modext.config import Config, ReprDict

from moddev.ntp import ntp_serv

from .valves import mod_valves

##todo
from .program import mod_programs
from .schedule import mod_scheduled
from .state import mod_state


def _dow():
    return ntp_serv.cron_dow()


def _time():
    return ntp_serv.localtime()


class Scheduler(Module, ReprDict):
    def watching_events(self):
        return ["ntp"]

    def init(self):
        self.info("register save callbacks")
        mod_programs.save_cb = self.recalc
        mod_scheduled.save_cb = self.recalc

    def conf(self, config=None):
        self.ntp = False

    def start(self):
        pass

    def stop(self):
        pass

    def __loop__(self, config=None, event=None, data=None):

        if self.current_level() != LifeCycle.RUNNING:
            return

        if event == "ntp":
            val = self.event_data_value(data)
            self.info("ntp", val)
            if val:
                self.recalc()
                self.ntp = True

        if self.ntp == False:
            return

        if self.dow != _dow():
            self.recalc()

        self.cron()

    def _format(self, now):
        return "{0:02d}:{1:02d}".format(now[3], now[4])

    def recalc(self):
        self.info("recalc")
        schedf = list(filter(lambda x: x.active, mod_scheduled.get_schedule()))
        self.dow = _dow()
        dayf = list(filter(lambda x: x.dow[self.dow], schedf))
        now = _time()
        nowf = self._format(now)
        timef = list(filter(lambda x: x.time >= nowf, dayf))

        programs = list(filter(lambda x: x.active, mod_programs.get_program_list()))
        program_ids = list(map(lambda x: x.id, programs))

        activef = list(filter(lambda x: x.program in program_ids, timef))

        sortf = list(sorted(activef, key=lambda x: x.time))

        mod_state.scheduled = sortf

    def cron(self):
        if len(mod_state.scheduled) == 0:
            return
        now = _time()
        nowf = self._format(now)
        if nowf >= mod_state.scheduled[0].time:
            self.info("cron task found")
            if mod_state.scheduler_pause == False:
                mod_state.play_schedule()
            else:
                self.info("pause mode, dump task")
                mod_state.scheduled.pop(0)

    def __repr__(self):
        return {
            "scheduled": self.reprlist(mod_state.scheduled),
        }


mod_scheduler = Scheduler("scheduler")
modc.add(mod_scheduler)
