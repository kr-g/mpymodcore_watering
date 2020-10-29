from machine import Pin

from modcore import modc, Module, LifeCycle
from modcore.log import LogSupport
from modext.config import Config, ReprDict

from moddev.ntp import ntp_serv

from .valves import mod_valves

##todo
from .program import mod_programs
from .schedule import mod_scheduled


def _time():
    return ntp_serv.time()


class StateTask(ReprDict):
    def __init__(self, duration):
        self.duration = duration
        self._start = None
        self._stop = None
        self.diff = 0
        self.state = False

        self.start()

    def start(self):
        self._start = _time()
        self._stop = self._start + self.duration
        self.diff = self._stop - self._start
        self.state = self.diff > 0
        return self

    def stop(self):
        self.duration = max(self._stop - _time(), 0)
        self._start = None
        self._stop = None
        self.state = False
        return self

    def chk_valid(self):
        if mod_state.scheduler_pause == True:
            return False
        now = _time()
        self.diff = self._stop - now
        self.state = self.diff > 0
        return self.state

    def __repr__(self):
        return {
            "diff": max(self.diff, 0),
        }


class State(Module, ReprDict):
    def conf(self, config=None):
        self.current = []
        self.curstates = []
        self.curtasks = []
        self.next = []
        self.scheduled = []
        self.state = True
        self.scheduler_pause = False
        self.info_text = ""

    def start(self):
        pass

    def stop(self):
        mod_valves.apply()

    def __loop_run__(self, config=None, event=None, data=None):

        if self.scheduler_pause == True:
            # pause on
            return

        if len(self.curstates) > 0:
            self.update_current()
            if not any(self.curstates):
                if len(self.next) > 0:
                    self.play_next()
                else:
                    self.apply_current()
                    self.curstates = []
                    self.current = []
        else:
            if len(self.next) > 0:
                self.play_next()

    def __repr__(self):
        return {
            "current": self.current,
            "curstates": self.curstates,
            "curtasks": self.reprlist(self.curtasks),
            "next": self.next,
            "scheduled": self.reprlist(self.scheduled),
            "state": self.state,
            "scheduler_pause": self.scheduler_pause,
            "info_text": self.info_text,
        }

    def pause_watering(self):
        self.info("pause_watering")
        # self.state = False
        self.scheduler_pause = True
        # mod_valves.set_pause(True)
        _ = list(map(lambda x: x.stop(), self.curtasks))
        self.apply_current()

    def resume_watering(self):
        self.info("resume_watering")
        # self.state = True
        self.scheduler_pause = False
        # mod_valves.set_pause(False)
        _ = list(map(lambda x: x.start(), self.curtasks))
        self.apply_current()

    def setup_current(self):
        ## todo refact
        self.curtasks = [StateTask(duration) for duration in self.current]

    def update_current(self):
        self.curstates = list(map(lambda x: x.chk_valid(), self.curtasks))

    def apply_current(self):
        ## todo refact
        self.update_current()
        mod_valves.apply(self.curstates)

    def play_next(self):
        self.current = []
        if len(self.next) > 0:
            self.current = self.next.pop(0)
            self.info("play_next", self.current)
            self.setup_current()
        self.apply_current()

    def remove_next(self, pos):
        if pos < len(self.next):
            self.next.pop(pos)

    def play_watering(self, program_tasks):
        self.next.extend(program_tasks)

    def play_schedule(self):
        sched = self.scheduled.pop(0)
        self.info("play_schedule", sched.id, sched.name, sched.program)
        program = mod_programs.get_program_by_id(sched.program)
        self.info("play_schedule", program.id, program.name)
        self.play_watering(program.get_tasks())


mod_state = State("state")
modc.add(mod_state)
