#
# this is a sample boot sequence, can be used as template to create own
#

# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import uos as os
import machine
import time

# uos.dupterm(None, 1) # disable REPL on UART(0)

import micropython

interrupts_enabled = False

if interrupts_enabled:
    micropython.alloc_emergency_exception_buf(128)

import gc

gc.collect()


def mem_info(verbose=True, auto_free=True):
    if auto_free:
        gc.collect()
    if verbose:
        micropython.mem_info(1)
    else:
        micropython.mem_info()
    return gc.mem_free()


def hardreset():
    machine.reset()


def gc_print_stat():
    before = gc.mem_free(), gc.mem_alloc()
    gc.collect()
    after = gc.mem_free(), gc.mem_alloc()
    print("(free,alloc)", "before", before)
    print("(free,alloc)", "after", after)


from modcore import modc, Module, LifeCycle
from modcore import DEBUG, INFO, NOTSET, logger

from moddev.control import control_serv

from moddev import wlan
from moddev.wlan import wlan_ap

from moddev import ntp
from moddev.ntp import ntp_serv, set_log_time

# ntp can change timezone dynamically
# press cntrl+c during loop and fire an event, then call loop() again
# modc.fire_event("tz", 3600*2 ) # 2 hours offset
# modc.fire_event("tz" ) # utc

from moddev import softap

from moddev import webrepl
from moddev.webrepl import webrepl_serv

from moddev.interval import Interval

session_purge = Interval("session_purge")
modc.add(session_purge)

live_ping = Interval("live_ping")
modc.add(live_ping)


from moddev.button import Button

boot_btn = Button("boot_btn")
modc.add(boot_btn)

# configuration data

cfg = {
    "TZ": 60 * 60 * 2,
    # led pin for ttgo board
    "led": 21,
    "live_ping": 5,  # timeout in sec, default timebase 1000
    "live_ping:event": ["pin:led:toggle"],  # access led parameter from cfg
    "session_purge": 30,
    "session_purge:timebase": 1000 * 60,  # 1 min timebase
    "session_purge:event": "session-man",  # event to fire
    "boot_btn": 0,  # pin no -> gpio 0
    "boot_btn:debounce": 100,  # 100ms - default, can be obmitted
    "boot_btn:neg_logic": True,  # boot button gpio0 becomes signaled with value 0 by pressing
    "boot_btn:fire_on_up": True,  # default, fires when releasing
    "boot_btn:event": [
        "pin:led:off",
        "break",
    ],  # raise 2 events
}

# enable winup session manager module
import modext.windup.session_mod

generators = []

logger.info("loading apps")
from modapp.watering import app_config, load_config, load_generators, mod_valves

APPNAME, watering_conf = app_config
cfg[APPNAME] = watering_conf
generators.extend(load_generators())

# add all modules to start automatically before this call
modc.startup(config=cfg)

# just serving some static files
from modext.windup import WindUp, Router

serv = WindUp()

import mod3rd
from mod3rd.admin_esp.wlan import router as router_wlan
from mod3rd.admin_windup.content import router as router_generators

logger.info("config done. start windup.")

run_not_in_sample_mode = True

if run_not_in_sample_mode:

    generators.extend(
        [
            router_wlan,
            router_generators,  # optional
        ]
    )

    serv.start(generators=generators)

import modext.misc.main as mod_main

mod_main.debug_mode = True


def loop():
    mod_main.loop(cfg, serv.loop)


loop()
