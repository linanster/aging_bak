#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess
from multiprocessing import Process
from flask import flash, redirect, url_for
from .mypymysql import cleanup_temp

from .tools import get_totalcount, reset_progress, add_progress


gofolder = os.path.join(os.getcwd(), 'go')


def async_call(fn):
    def wrapper(*args, **kwargs):
        Process(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

# @async_call
def start():
    reset_progress()
    cmdlist = [_start, _changemesh, _scan, _bulb_cmd_set]
    for cmd in cmdlist:
        errno = cmd()
        if errno != 0:
            return errno
        else:
            add_progress()
            time.sleep(5)
        
    return 0


def blink_single(mac):
    segments = mac.split(':')
    maclist = segments[4] + segments[5]
    p = subprocess.Popen("./ble-backend -command=nok_ident -maclist={}".format(maclist), shell=True, cwd=gofolder)
    p.wait()
    return 0


def blink_all():
    p = subprocess.Popen("./ble-backend -command=nok_ident -maclist=ffff", shell=True, cwd=gofolder)
    p.wait()
    return 0
    
def blink_stop():
    p = subprocess.Popen("./ble-backend -command=nok_ident -maclist=stop", shell=True, cwd=gofolder)
    p.wait()
    return 0

def _start():
    loop = 1
    while 0 != subprocess.call("./ble-backend -command=start -meshname=telink_mesh7 -meshpass=123", shell=True, cwd=gofolder):
        if loop==3:
            return -1
        loop+=1
    return 0
    
def _changemesh():
    loop = 1
    while 0 != subprocess.call("./ble-backend -command=changemesh  -meshname=telink_mesh7 -meshpass=123", shell=True, cwd=gofolder):
        if loop==3:
            return -2
        loop+=1
    return 0

def _scan():
    num = get_totalcount()
    return subprocess.call("./ble-backend -command=scan -totalcount={}".format(num), shell=True, cwd=gofolder)
    # loop = 1
    # while 0 != subprocess.call("./ble-backend -command=scan -totalcount={}".format(num), shell=True, cwd=gofolder):
    #     if loop==3:
    #         return -3
    #     loop+=1
    # return 0

def _bulb_cmd_set():
    while 0 != subprocess.call("./ble-backend -command=bulb_cmd_set1", shell=True, cwd=gofolder):
        if loop==3:
            return -4
        loop+=1
    return 0
