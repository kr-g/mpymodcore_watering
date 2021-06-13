"""
(c) 2020 K. Goger (k.r.goger@gmail.com)

https://github.com/kr-g/mpymodcore_watering

License under:
https://github.com/kr-g/mpymodcore_watering/blob/master/LICENSE

"""

VERSION = "v0.0.10"
APPNAME = "watering"

from .app import load_config, load_generators, app_config
from .valves import mod_valves
from .settings import mod_settings
from .program import mod_programs, reload_programs
from .schedule import mod_scheduled, reload_schedule
from .state import mod_state
from .scheduler import mod_scheduler
from .autorestart import mod_autorestart
from .flow_meter import mod_flowmeter

print("-" * 41)
print("mpy modcore " + APPNAME)
print("(c) 2020 K. Goger")
print("version  ", VERSION)
print("homepage ", "https://github.com/kr-g/mpymodcore_watering")
print("legal    ", "https://github.com/kr-g/mpymodcore_watering/blob/master/LICENSE")
print("-" * 41)
