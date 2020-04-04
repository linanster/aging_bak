#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess
from multiprocessing import Process
from threading import Thread, Lock
from flask import flash, redirect, url_for

from .execsql import testdatas_cleanup, get_running_state_sql
from .execsql import get_retried_sql, set_retried_sql, reset_retried_sql

from .tools import get_totalcount
from .tools import reset_progress, add_progress
from .tools import reset_running_state, set_running_state, get_running_state
from .tools import reset_phase, set_phase
from .tools import reset_errno, set_errno

from app.ext.mysocketio import socketio
from flask_socketio import send

from app.settings import Debug
from app.settings import Timeout


# gofolder = os.path.join(os.getcwd(), 'go')
topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
gofolder = os.path.abspath(os.path.join(topdir, "go"))


thread = None
thread_lock = Lock()


def async_call(fn):
    def wrapper(*args, **kwargs):
        Process(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

def ThreadMaker(f):
    def runner(*args, **argv):
        Thread(target=f, args=args, kwargs=argv).start()
    return runner

@ThreadMaker
def test():
    time.sleep(5)
    print('socketio emit event1')
    socketio.emit('event_done', namespace='/ns2')

@ThreadMaker
def watch_to_jump():
    while True:
        if get_running_state_sql():
            print('wait')
            if get_retried_sql():
                newline = 1
                reset_retried_sql()
            else:
                newline = 0
            socketio.emit('progress', {'data': '+', 'newline': newline}, namespace='/test', broadcast=True)
            time.sleep(2)
        else:
            print('emit event_done')
            socketio.emit('event_done', namespace='/test', broadcast=True)
            break
    
@async_call
def start():
    testdatas_cleanup()
    reset_errno()
    set_running_state()
    num = get_totalcount()
    loop = 1
    while loop <= 3:
        errno = subprocess.call("./ble-backend -command=starttest -totalcount={}".format(num), shell=True, cwd=gofolder)
        loop += 1
        if errno == 0:
            # todo
            errno = 0
            if Debug:
                print('==starttest success==') 
                print('==errno==',errno)
            break
        else:
            # todo
            errno = -1
            time.sleep(Timeout)
            subprocess.call("./ble-backend -command=allkickout", shell=True, cwd=gofolder)
            set_retried_sql()
            continue
    if Debug and loop > 3 :
        print('==starttest failed==') 
        print('==errno==',errno)
    reset_running_state()
    set_errno(errno)
    return errno
    

@async_call
def start_legacy():
    testdatas_cleanup()
    set_running_state()
    reset_progress()
    reset_phase()
    reset_errno()
    cmdlist = [_start, _changemesh, _scan]
    for cmd in cmdlist:
        errno = cmd()
        if errno != 0:
            if Debug:
                print('==task failed==')
            reset_running_state()
            return errno
        else:
            add_progress()

    _bulb_cmd_set()    
    reset_running_state()
    if Debug:
        print('==task complete==')
        print('')
    return 0


def blink_single(mac):
    segments = mac.split(':')
    maclist = segments[4] + segments[5]
    loop = 1
    while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist={}".format(maclist), shell=True, cwd=gofolder):
        time.sleep(Timeout)
        if loop==3:
            if Debug:
                print('==blink_single failed==') 
            return -1
        loop+=1
    if Debug:
        print('==blink_single success==')
    return 0


def blink_all():
    loop = 1
    while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist=ffff", shell=True, cwd=gofolder):
        time.sleep(Timeout)
        if loop==3:
            if Debug:
                print('==blink_all failed==') 
            return -1
        loop+=1
    if Debug:
        print('==blink_all success==')
    return 0
    
def blink_stop():
    loop = 1
    while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist=stop", shell=True, cwd=gofolder):
        time.sleep(Timeout)
        if loop==3:
            if Debug:
                print('==blink_stop failed==') 
            return -1
        loop+=1
    if Debug:
        print('==blink_stop success==')
    return 0

def _start():
    set_phase('_start')
    loop = 1
    # todo
    while 0 != subprocess.call("./ble-backend -command=start -meshname=telink_mesh7 -meshpass=123", shell=True, cwd=gofolder):
    # while 0 != subprocess.call("./ble-backend -command=start", shell=True, cwd=gofolder):
        time.sleep(Timeout)
        if loop==3:
            if Debug:
                print('==_start failed==') 
            set_errno(-1)
            return -1
        loop+=1
    if Debug:
        print('==_start success==')
    return 0
    
def _changemesh():
    set_phase('_changemesh')
    loop = 1
    # todo
    while 0 != subprocess.call("./ble-backend -command=changemesh -meshname=telink_mesh7 -meshpass=123", shell=True, cwd=gofolder):
    # while 0 != subprocess.call("./ble-backend -command=changemesh", shell=True, cwd=gofolder):
        time.sleep(Timeout)
        if loop==3:
            if Debug:
                print('==_changemesh failed==') 
            set_errno(-2)
            return -2
        loop+=1
    if Debug:
        print('==_changemesh success==')
    return 0

def _scan():
    set_phase('_scan')
    num = get_totalcount()
    errno = subprocess.call("./ble-backend -command=scan -totalcount={}".format(num), shell=True, cwd=gofolder)
    if errno != 0:
        if Debug:
            print('==_scan failed==') 
        set_errno(-3)
        return -3
    time.sleep(Timeout)
    if Debug:
        print('==_scan success==')
    return 0

# regardless of _bulb_cmd_set
@async_call
def _bulb_cmd_set():
    set_phase('_bulb_cmd_set')
    loop = 1
    while 0 != subprocess.call("./ble-backend -command=bulb_cmd_set1", shell=True, cwd=gofolder):
        time.sleep(Timeout)
        if loop==3:
            if Debug:
                print('==_bulb_cmd_set failed==') 

            # regardless of _bulb_cmd_set
            # set_errno(-4)
            return -4
        loop+=1
    if Debug:
        print('==_bulb_cmd_set success==')
    return 0
