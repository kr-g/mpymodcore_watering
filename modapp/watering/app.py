from modcore import modc, VERSION as modcore_version
from modcore.log import LogSupport

from modext.config import Config, Namespace
from modext.windup.content import StaticFiles
from modext.windup import Router

from .settings import mod_settings
from .valves import mod_valves
from .program import mod_programs, reload_programs
from .schedule import mod_scheduled, reload_schedule
from .scheduler import mod_scheduler
from .state import mod_state
from .autorestart import mod_autorestart
from .flow_meter import mod_flowmeter

import sys
import time
import machine
import gc
import binascii
from moddev.wlan import wlan_ap
from moddev.softap import soft_ap
from moddev.ntp import ntp_serv
from moddev.control import RESTART, EXIT, BREAK


logger = LogSupport()
logger.logname = mod_settings.app


system = Router("/system")


@system.get("/gc")
def run_gc(req, args):
    gc.collect()
    info = {
        "time": time.time(),
        "mem_free": gc.mem_free(),
        "mem_alloc": gc.mem_alloc(),
    }
    req.send_json(info)


@system.get("/ping")
def ping_get(req, args):
    req.send_json(
        {
            "ping": "pong",
        }
    )


"""
@system.get("/exit")
def ping_get(req,args):
    sys.ecit()
    req.send_json( { "ping" : "pong", } )
"""


@system.get("/info")
def info(req, args):

    t = time.time()

    info = {
        "time": t,
        "timezone_offset": ntp_serv.offset,
        "localtime_offset": ntp_serv.offset,
        "localtime": list(time.localtime(t)),
        "localtime_tz": list(time.localtime(t + ntp_serv.offset)),
        "unique_id": binascii.hexlify(machine.unique_id()).decode(),
        "freq": machine.freq(),
        "mem_free": gc.mem_free(),
        "mem_alloc": gc.mem_alloc(),
        "modcore_version": modcore_version,
        "app": mod_settings.app,
        "app_version": mod_settings.version,
        "softap": {
            "active": soft_ap.active(),
            "mac": binascii.hexlify(soft_ap.mac()).decode(),
            "ip": list(soft_ap.ifconfig()),
        },
        "wlan": {
            "active": wlan_ap.active(),
            "mac": binascii.hexlify(wlan_ap.mac()).decode(),
            "ip": list(wlan_ap.ifconfig()),
        },
    }
    req.send_json(info)


@system.get("/timezone")
def timezone_get(req, args):
    info = {
        "timezone_offset": ntp_serv.offset,
    }
    req.send_json(info)


@system.post("/timezone")
def timezone_post(req, args):
    tz_off = args.json.timezone_offset
    logger.info(tz_off)
    ntp_serv.set_tz_offset(tz_off)
    # scheduler listens on ntp event
    req.send_response()


@system.get("/config")
def reboot_config_get(req, args):
    config = mod_settings.config()
    req.send_json({"config": dict(config)})


@system.get("/reboot/config")
def reboot_config_get(req, args):
    autorestart = mod_autorestart.get_autorestart()
    req.send_json(
        {
            "reboot": {
                "active": autorestart != None,
                "time": autorestart,
            }
        }
    )


@system.post("/reboot/config")
def reboot_config_post(req, args):
    reboot = args.json.reboot
    logger.info(reboot)
    mod_autorestart.save(reboot.time if reboot.active else None)
    req.send_response()


@system("/reboot/:type", xtract=True)
def reboot_post(req, args):
    par = args.rest
    logger.info("reboot", par)
    modc.fire_event(RESTART, par.type)
    req.send_response()


@system("/exit")
def exit_post(req, args):
    mod_state.pause_watering()
    modc.fire_event(EXIT)
    req.send_response()


@system("/break")
def break_post(req, args):
    mod_state.pause_watering()
    modc.fire_event(BREAK)
    req.send_response()


router = Router("/watering")


@router.get("/valves/config")
def valves_config_get(req, args):
    logger.info(mod_valves.ports)
    req.send_json(mod_valves.reprlist(mod_valves.config.valves))


@router.post("/valves/config")
def valves_config_post(req, args):
    logger.info(args.json)
    ns = Namespace()
    ns.valves = args.json.valves
    mod_valves.save(ns.valves)
    req.send_response()


@router.get("/valves")
def valves_get(req, args):
    logger.info(mod_valves.ports)
    req.send_json(mod_valves.reprlist(mod_valves.ports))


@router.post("/valves")
def valves_post(req, args):
    logger.info(args.json)
    logger.info("!!!not implemented!!!")
    req.send_response()


@router.xpost("/valve/:port/:state")
def valve_post(req, args):
    par = args.rest
    logger.info(par)
    port = int(par.port)
    if port < 0 or port > len(mod_valves.ports):
        raise Exception("invalid port", port)

    mod_state.scheduler_pause = True
    states = list(map(lambda x: x.get_state(), mod_valves.ports))

    state = par.state.lower() == "true"
    states[port] = state

    mod_valves.apply(states)

    req.send_response()


@router.xget("/valve/:port")
def valve_get(req, args):
    par = args.rest
    logger.info(par)
    port = int(par.port)
    if port < 0 or port > len(mod_valves.ports):
        raise Exception("invalid port", port)
    valve = mod_valves.ports[port]
    req.send_json(
        {
            "valve": dict(valve),
            "port": port,
        }
    )


@router.get("/programs")
def programs_get(req, args):
    reload_programs()
    req.send_json(mod_programs.get_programs())


@router.post("/programs")
def programs_post(req, args):
    par = args.json
    logger.info(par)
    mod_programs.save(par)
    req.send_response()


@router.xpost("/program/play/:pos")
def program_play_post(req, args):
    par = args.rest
    logger.info(par)
    pos = int(par.pos)
    logger.info(pos)
    mod_state.play_watering(mod_programs.get_program(pos).get_tasks())
    req.send_response()


@router.get("/scheduled")
def scheduled_get(req, args):
    reload_schedule()
    req.send_json(mod_scheduled.get_scheduled())


@router.post("/scheduled")
def scheduled_post(req, args):
    par = args.json
    logger.info(par)
    mod_scheduled.save(par)
    req.send_response()


@router("/scheduled/recalc")
def scheduled_recalc_post(req, args):
    mod_scheduler.recalc()
    req.send_response()


@router.get("/state")
def state_get(req, args):
    logger.info("state")
    req.send_json(dict(mod_state))


@router.get("/state/info")
def state_get(req, args):
    logger.info("state")
    req.send_json(
        {
            "info_text": mod_state.info_text,
        }
    )


@router.post("/state/kill")
def state_kill_post(req, args):
    mod_state.play_next()
    req.send_response()


@router.xpost("/state/remove/:pos")
def state_remove_post(req, args):
    par = args.rest
    logger.info(par)
    pos = int(par.pos)
    logger.info(pos)
    mod_state.remove_next(pos)
    req.send_response()


@router.xget("/pause/:pause")
def state_kill_post(req, args):
    pause = args.rest.pause.lower() == "true"
    if pause:
        mod_state.pause_watering()
    else:
        mod_state.resume_watering()
    mod_scheduler.pause = pause
    req.send_json({"state": mod_state.state})


@router.get("/flow")
def flowmeter_get(req, args):
    logger.info("state")
    req.send_json(
        {
            "flow": dict(mod_flowmeter),
        }
    )


@router.post("/flow/config")
def flowmeter_post(req, args):
    par = args.json
    logger.info(par)

    mod_flowmeter.save(par.flow)
    mod_flowmeter.reconfigure()

    req.send_response()


def load_config():

    valves_cfg = mod_valves.config  # ()
    settings_cfg = mod_settings.config()

    app_cfg = Namespace()
    app_cfg.update(valves_cfg)
    app_cfg.update(settings_cfg)

    return mod_settings.app, app_cfg


app_config = load_config()


def load_generators():
    return [
        StaticFiles(
            ["/modapp/" + mod_settings.app + "/www"],
            root="/static/" + mod_settings.app,
            send_buffer=512,
        ),
        router,
        system,
    ]
