from machine import Pin

from modcore import modc, Module, LifeCycle
from modcore.log import LogSupport

from moddev.timeout import Timeout

from modext.irq import Counter
from modext.config import Config, ReprDict

from .state import mod_state
from .settings import mod_settings


class FlowMeter(Module, ReprDict):
    def init(self):
        self.total = 0
        self.cnt = 0

    def conf(self, config=None):
        self.counter = Counter(self.config.flow.pin)
        self.timeout = Timeout(
            timeout=self.config.flow.time_out, timebase=self.config.flow.time_base
        )

    def start(self):
        self.counter.enable()
        self.timeout.restart()

    def __loop_run__(self, config=None, event=None, data=None):
        if self.timeout.elapsed() == False:
            return
        self.cnt = self.counter.count
        self._reset_count()
        self.total += self.cnt
        if self.config.flow.max > 0 and self.cnt > self.config.flow.max:
            mod_state.pause_watering()
            ## todo pause watering
            ## set status
        self.timeout.restart()

    def stop(self):
        self.counter.disable()

    def __repr__(self):
        return {
            "pin": self.config.flow.pin,
            "total": self.total,
            "total_liter": self.estimate_total_liter(),
            "current": self.cnt,
            "current_liter": self.estimate_liter(),
            "max": self.config.flow.max,
            "liter_ratio": self.config.flow.liter_ratio,
            "time_out": self.config.flow.time_out,
            "time_base": self.config.flow.time_base,
        }

    def _reset_count(self):
        self.counter.reset()

    def estimate_total_liter(self):
        return self.total * self.config.flow.liter_ratio

    def estimate_liter(self):
        return self.cnt * self.config.flow.liter_ratio

    def load(self):
        self.config = Config("/etc/" + mod_settings.app + "/flowmeter.json.txt")
        try:
            self.config.load()
        except Exception as ex:
            self.excep(ex, "no config found, load defaults")
            self.config.load(
                "/modapp/" + mod_settings.app + "/etc/flowmeter.template.json.txt"
            )
        return self

    def save(self, flow):
        self.config.flow.pin = flow.pin
        self.config.flow.max = flow.max
        self.config.flow.liter_ratio = flow.liter_ratio
        self.config.flow.time_out = flow.time_out
        self.config.flow.time_base = flow.time_base
        ## todo restart module

        self.config.save()


mod_flowmeter = FlowMeter("flowmeter").load()
modc.add(mod_flowmeter)
