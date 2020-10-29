from machine import Pin

from modcore import modc, Module, LifeCycle
from modcore.log import LogSupport
from modext.config import Config, ReprDict

from .settings import mod_settings


class Valve(LogSupport, ReprDict):
    def __init__(self, pin, name=None, disabled=False, sim=False):
        LogSupport.__init__(self)
        self.pin = pin
        self.name = name
        self.disabled = disabled
        self.error = False
        self.state = False
        self.pause = False

        if self.pin > 0 and not sim:
            self.port = Pin(pin, Pin.OUT)
            self.port.off()
        else:
            self.port = None

    def reset(self):
        self.error = False
        self.state = False
        self.pause = False
        self.apply()

    def set_pause(self, pause=True):
        self.pause = pause
        self.apply()

    def set_error(self, error=True):
        self.error = error
        self.apply()

    def apply(self, state=None):
        if state != None:
            self.state = state
        if self.disabled:
            self.warn("disabled port", self, state)
            return
        if self.port:
            self.port.value(self.get_state())
        else:
            self.info("simulate", self)

    def get_state(self):
        return self.state and not self.error and not self.pause

    def __repr__(self):
        return {
            "pin": self.pin,
            "name": self.name,
            "disabled": self.disabled,
            "error": self.error,
            "state": self.state,
            "pause": self.pause,
            "result": self.get_state(),
        }


class Valves(Module, ReprDict):
    def init(self):
        pass

    def conf(self, config=None):
        self.info("config", self.config)
        self.pins = list(map(lambda x: x.pin, self.config.valves))
        self.info("pins", self.pins)
        self.ports = list(
            map(
                lambda x: Valve(
                    x.pin,
                    name=x.name,
                    disabled=x.disabled,
                    # sim=True # !!! simulate always
                ),
                self.config.valves,
            )
        )
        self.info("ports", self.ports)

    def apply(self, states=None):
        self.info("apply state")
        if states == None or len(states) == 0:
            states = [False for x in range(0, len(self.ports))]
        for port, state in zip(self.ports, states):
            port.apply(state)

    def set_pause(self, pause=True):
        for port in self.ports:
            port.set_pause(pause)

    def start(self):
        self.apply()

    def stop(self):
        self.apply(False)

    def __repr__(self):
        return {
            "config": dict(self.config),
            "pins": self.pins,
            "no_ports": len(self.ports),
            "ports": self.reprlist(self.ports),
        }

    def load(self):
        self.config = Config("/etc/" + mod_settings.app + "/valves.json.txt")
        try:
            self.config.load()
        except Exception as ex:
            self.excep(ex, "no config found, load defaults")
            self.config.load(
                "/modapp/" + mod_settings.app + "/etc/valves.template.json.txt"
            )
        return self

    def save(self, valves):
        self.config.valves = self.reprlist(valves)

        import json

        s = json.dumps(self.config.valves)
        self.info("json", s)

        self.config.save()
        # self.conf()


#    def config(self):
#        return self.config


mod_valves = Valves("valves").load()
modc.add(mod_valves)
