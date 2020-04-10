#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess
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
from app.settings import gofolder
from app.settings import logfolder

from .mylogger import logger
from .mydecorator import processmaker, threadmaker



def _mysubprocess(cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=gofolder)
        while p.poll() is None:
            output = p.stdout.readline().decode('utf-8')[0:-1]
            logger.info('[ble-backend] {}'.format(output))
        errno = p.poll()
        if errno != 0:
            errmsg = p.stderr.read().decode('utf-8')[:-1]
            logger.error('[ble-backend] {}'.format(errmsg))
            logger.error('[ble-backend] errno:{}'.format(errno))
        p.stdout.close()
        p.stderr.close()
        return errno

@threadmaker
def watch_to_jump():
    while True:
        if get_running_state_sql():
            if get_retried_sql():
                newline = 1
                reset_retried_sql()
            else:
                newline = 0
            socketio.emit('progress', {'data': '+', 'newline': newline}, namespace='/test', broadcast=True)
            time.sleep(2)
        else:
            logger.info('==emit event_done==')
            socketio.emit('event_done', namespace='/test', broadcast=True)
            break
    
@processmaker
def start():
    logger.info('')
    logger.info('')
    logger.info('')
    logger.info('==starttest begin==')
    testdatas_cleanup()
    reset_errno()
    set_running_state()
    num = get_totalcount()
    loop = 1
    while loop <= 3:
        # METHOD-1
        # errno = subprocess.call("./ble-backend -command=starttest -totalcount={}".format(num), shell=True, cwd=gofolder)

        # METHOD-2
        # p = subprocess.Popen("./ble-backend -command=starttest -totalcount={}".format(num), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=gofolder)
        # output = p.communicate()
        # output_stdout = output[0].decode('utf-8')
        # output_stderr = output[1].decode('utf-8')
        # errno = p.poll()
        # print(output_stdout)
        # print(output_stderr)

        # METHOD-3
        # p = subprocess.Popen("./ble-backend -command=starttest -totalcount={}".format(num), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=gofolder)
        # while p.poll() is None:
        #     output = p.stdout.readline().decode('utf-8')[0:-1]
        #     print(output)
        # errno = p.poll()
        # if errno != 0:
        #     errmsg = p.stderr.read().decode('utf-8')[:-1]
        #     print(errmsg)
        #     print(errno)
        # p.stdout.close()
        # p.stderr.close()        

        # METHOD-4
        errno = _mysubprocess("./ble-backend -command=starttest -totalcount={}".format(num))

        loop += 1
        if errno == 0:
            # todo
            errno = 0
            break
        else:
            testdatas_cleanup()
            # todo
            errno = 1
            time.sleep(Timeout)
            # subprocess.call("./ble-backend -command=allkickout", shell=True, cwd=gofolder)
            _mysubprocess("./ble-backend -command=allkickout")
            set_retried_sql()
            continue
    # if loop > 3 :
    if errno == 0:
        logger.info('==starttest success==') 
        logger.info("==errno:{}==".format(errno))
    else:
        logger.error('==starttest failed==') 
        logger.error("==errno:{}==".format(errno))
    reset_running_state()
    set_errno(errno)
    return errno
    

@processmaker
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
    # while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist={} -meshname=telink_mesh1 -meshpass=123".format(maclist), shell=True, cwd=gofolder):
    while 0 != _mysubprocess("./ble-backend -command=nok_ident -maclist={} -meshname=telink_mesh1 -meshpass=123".format(maclist)):
        time.sleep(Timeout)
        if loop==3:
            logger.error('==blink_single failed==') 
            return -1
        loop+=1
    logger.info('==blink_single success==')
    return 0


def blink_all():
    loop = 1
    # while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist=ffff -meshname=telink_mesh1 -meshpass=123", shell=True, cwd=gofolder):
    while 0 != _mysubprocess("./ble-backend -command=nok_ident -maclist=ffff -meshname=telink_mesh1 -meshpass=123"):
        time.sleep(Timeout)
        if loop==3:
            logger.error('==blink_all failed==') 
            return -1
        loop+=1
    logger.info('==blink_all success==')
    return 0
    
def blink_stop():
    loop = 1
    # while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist=stop -meshname=telink_mesh1 -meshpass=123", shell=True, cwd=gofolder):
    while 0 != _mysubprocess("./ble-backend -command=nok_ident -maclist=stop -meshname=telink_mesh1 -meshpass=123"):
        time.sleep(Timeout)
        if loop==3:
            logger.error('==blink_stop failed==') 
            return -1
        loop+=1
    logger.info('==blink_stop success==')
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
@processmaker
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
