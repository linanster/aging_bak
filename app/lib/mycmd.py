#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess
from multiprocessing import Process
from flask import flash, redirect, url_for
from .mypymysql import cleanup_temp

from .tools import get_totalcount


gofolder = os.path.join(os.getcwd(), 'go')


def async_call(fn):
    def wrapper(*args, **kwargs):
        Process(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

# @async_call
def start():
    num = get_totalcount()
    p = subprocess.Popen("./ble-backend -command=start ", shell=True, cwd=gofolder)
    p.wait()
    p = subprocess.Popen("./ble-backend -command=changemesh", shell=True, cwd=gofolder)
    p.wait()
    p = subprocess.Popen("./ble-backend -command=scan -totalcount={}".format(num), shell=True, cwd=gofolder)
    p.wait()
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
