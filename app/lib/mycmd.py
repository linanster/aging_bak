#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess
from multiprocessing import Process
from flask import flash, redirect, url_for
from .mypymysql import migrate_to_stage, migrate_to_archive, cleanup_temp, cleanup_stage

from .tools import get_running_state, set_running_state, reset_running_state
from .tools import get_paused_state, set_paused_state, reset_paused_state
from .tools import get_stop_action, set_stop_action, reset_stop_action


TEST = True
program = "./ble-backend-nan" if TEST else "./ble-backend"

gofolder = os.path.join(os.getcwd(), 'go')


def async_call(fn):
    def wrapper(*args, **kwargs):
        Process(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

@async_call
def start(devicecode, factoryid):
    set_running_state()
    reset_stop_action()
    # 1. Start "ble-bakcend -command=start", and then waiting 60 seconds.
    _start()
    # time.sleep(60)
    time.sleep(6)
    # 2. Start "ble-backend -command=changemesh", and then waiting for 30 seconds.
    _changemesh()
    # time.sleep(30)
    time.sleep(3)
    # 3. loop run "ble-backend --command=scan", in every 10 seconds

    while True:
        if get_stop_action():
            reset_running_state()
            break
        else:
            cleanup_temp()
            _scan(devicecode, factoryid)
            time.sleep(10)
    return 0

# @async_call
def stop():
    set_stop_action()
    while True:
        if get_running_state():
            time.sleep(1)
        else:
            break
    return 0
    

# @async_call
def turn_on_off(mac, on_off):
    try:
        print('turn {} {} start'.format(on_off, mac))
        p = subprocess.Popen("{} -command={} -mac={}".format(program, on_off, mac), shell=True, cwd=gofolder)
        # wait till on/off command finished
        p.wait()
    except Exception as e:
        print('turn_on_off error:', str(e))
        return 1
    else:
        print('turn {} {} complete'.format(on_off, mac))
        return 0

@async_call
def _start():
    try:
        print('start start...')
        # print os.getcwd() - /git/aging/flask
        p = subprocess.Popen("{} -command=start".format(program), shell=True, cwd=gofolder)
    except Exception as e:
        print("start error:",str(e))
        return 1
    else:
        print("start success")
        return 0

@async_call
def _changemesh():
    try:
        print('changemesh start...')
        p = subprocess.Popen("{} -command=changemesh".format(program), shell=True, cwd=gofolder)
    except Exception as e:
        print("change mesh error:", str(e))
        return 1
    else:
        print("change mesh success")
        return 0
    
@async_call
def _scan(devicecode, factoryid):
    print('scan start...')
    p = subprocess.Popen("{} -command=scan -devicecode={} -factoryid={}".format(program, devicecode, factoryid), shell=True, cwd=gofolder)
    # p.wait()

    
