#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess
from multiprocessing import Process
from flask import flash, redirect, url_for
from .mypymysql import cleanup_temp

from .tools import get_running_state, set_running_state, reset_running_state


TEST = True
program = "./ble-backend-nan" if TEST else "./ble-backend"

gofolder = os.path.join(os.getcwd(), 'go')


def async_call(fn):
    def wrapper(*args, **kwargs):
        Process(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

# @async_call
def start():
    _start()
    time.sleep(1)
    _changemesh()
    time.sleep(1)
    _scan()
    time.sleep(1)

    return 0


# @async_call
def turn_on_off(mac, on_off):
    print('turn {} {} start'.format(on_off, mac))
    p = subprocess.Popen("{} -command={} -mac={}".format(program, on_off, mac), shell=True, cwd=gofolder)
    # wait till on/off command finished
    p.wait()

# @async_call
def _start():
    print('start start...')
    p = subprocess.Popen("{} -command=start".format(program), shell=True, cwd=gofolder)
    return 0

# @async_call
def _changemesh():
    print('changemesh start...')
    p = subprocess.Popen("{} -command=changemesh".format(program), shell=True, cwd=gofolder)
    
# @async_call
def _scan():
    print('scan start...')
    p = subprocess.Popen("{} -command=scan".format(program), shell=True, cwd=gofolder)
    # p.wait()

    
