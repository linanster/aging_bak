#! /usr/bin/env python3
# coding: utf8
#
from flask import flash, redirect, url_for, send_from_directory
import time
import os
import subprocess
import datetime
from sqlalchemy import or_, and_

from .execsql import get_running_state_sql, reset_running_state_sql
from .execsql import get_retried_sql, set_retried_sql, reset_retried_sql

from app.lib.execmodel import testdatas_cleanup

from .tools import get_totalcount, get_devicecode, get_fwversion, get_mcuversion, get_ble_strength_low, get_wifi_strength_low
from .tools import reset_progress, add_progress
from .tools import reset_running_state, set_running_state, get_running_state
from .tools import reset_phase, set_phase
from .tools import reset_errno, set_errno

from app.ext.mysocketio import socketio
from flask_socketio import send

from app.myglobals import Debug, Timeout
from app.myglobals import gofolder, logfolder

from .mylogger import logger_app
from .mydecorator import processmaker, threadmaker
from .myutils import gen_excel

from app.models.mysql import Testdata


def _gosubprocess(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=gofolder)
    while p.poll() is None:
        output = p.stdout.readline().decode('utf-8')[0:-1]
        logger_app.info('[ble-backend] {}'.format(output))
    errno = p.poll()
    if errno != 0:
        errmsg = p.stderr.read().decode('utf-8')[:-1]
        logger_app.error('{ble-backend] errno: {}'.format(errno))
        logger_app.error('[ble-backend] {}'.format(errmsg))
    p.stdout.close()
    p.stderr.close()
    return errno


@processmaker
def watch_timeout():
    mytimer = 300 # seconds
    while True:
        if get_running_state():
            if mytimer > 0:
                time.sleep(2)
                mytimer = mytimer - 2
            else:
                logger_app.info('==watch timeout: timeout and reset==')
                reset_running_state()
                break
        else:
            logger_app.info('==watch tiemout: running state changed and nothing to do==')
            break
    return 0

@threadmaker
def watch_to_jump():
    while True:
        if get_running_state_sql():
            # socketio.sleep(2)
            time.sleep(2)
        else:
            logger_app.info('==detect running state finished, emit event done==')
            socketio.emit('mydone', namespace='/test', broadcast=True)
            break
    return 0

def watch_to_finish():
    while True:
        if get_running_state():
            time.sleep(2)
        else:
            logger_app.info('==detect running state finished, notice api to return==')
            break
    return 0

@processmaker
def watch_to_blink():
    while True:
        if get_running_state():
            time.sleep(2)
        else:
            logger_app.info('==detect running state finished, blink all failed bulbs==')
            blink_failed()
            break
    return 0

    
@processmaker
def start():
    # reserve time for frontend to receive event message
    time.sleep(3)
    logger_app.info('==测试开始==')
    logger_app.info('==starttest begin==')
    testdatas_cleanup()
    reset_errno()
    set_running_state()

    devicecode = get_devicecode()
    totalcount = get_totalcount()
    fwversion = get_fwversion()
    mcuversion = get_mcuversion()
    ble_strength_low = get_ble_strength_low()
    wifi_strength_low = get_wifi_strength_low()

    logger_app.info('==config devicecode: %s==' % devicecode)
    logger_app.info('==config totalcount: %s==' % totalcount)
    logger_app.info('==config fwversion: %s==' % fwversion)
    logger_app.info('==config mcuversion: %s==' % mcuversion)
    logger_app.info('==config ble_strength_low: %s==' % ble_strength_low)
    logger_app.info('==config wifi_strength_low: %s==' % wifi_strength_low)
    # return, if either is not set by test_config setp
    if totalcount is None or devicecode is None or fwversion is None:
        errno = 2
        reset_running_state()
        set_errno(errno)
        return errno

    loop = 1
    # while loop <= 3:
    while loop <= 1:
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
        # errno = _gosubprocess("./ble-backend -command=starttest -totalcount={} -deviceid={} -fwversion={} -mcuversion={}".format(totalcount, devicecode, fwversion, mcuversion))
        errno = _gosubprocess("./ble-backend -command=starttest")

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
            _gosubprocess("./ble-backend -command=allkickout")
            set_retried_sql()
            continue
    if errno == 0:
        logger_app.info('==starttest success==') 
        logger_app.info("==errno:{}==".format(errno))
    else:
        logger_app.error('==starttest failed==') 
        logger_app.error("==errno:{}==".format(errno))
    # reserve time for frontend to receive event message
    time.sleep(3)
    reset_running_state()
    set_errno(errno)
    logger_app.info('==测试结束==')
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
    macseg = segments[4] + segments[5]
    loop = 1
    # while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist={}".format(macseg), shell=True, cwd=gofolder):
    while 0 != _gosubprocess("./ble-backend -command=nok_ident -maclist={}".format(macseg)):
        # time.sleep(Timeout)
        # if loop==3:
        if loop==1:
            logger_app.error('==blink_single failed==') 
            return -1
        loop+=1
    logger_app.info('==blink_single success==')
    return 0

def blink_group(macs):
    macgroups = [macs[i:i+4] for i in range(0, len(macs), 4)]
    # print('==macgroups==', macgroups)
    macsegs = list()
    for macgroup in macgroups:
        # print('==macgroup==', macgroup)
        macseg = str()
        for mac in macgroup:
            parts = mac.split(':')
            macseg += (parts[4] + parts[5])
        macsegs.append(macseg)
    # print('==macsegs==', macsegs)

    for macseg in macsegs:
        loop = 1
        # while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist={}".format(macseg), shell=True, cwd=gofolder):
        while 0 != _gosubprocess("./ble-backend -command=nok_ident -maclist={}".format(macseg)):
            # time.sleep(Timeout)
            # if loop==3:
            if loop==1:
                logger_app.error('==blink_group failed==')
                return -1
            loop+=1
        logger_app.info('==blink_group success==')
    return 0


def blink_all():
    loop = 1
    # while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist=ffff", shell=True, cwd=gofolder):
    while 0 != _gosubprocess("./ble-backend -command=nok_ident -maclist=ffff"):
        # time.sleep(Timeout)
        # if loop==3:
        if loop==1:
            logger_app.error('==blink_all failed==') 
            return -1
        loop+=1
    logger_app.info('==blink_all success==')
    return 0
    
def blink_stop():
    loop = 1
    # while 0 != subprocess.call("./ble-backend -command=nok_ident -maclist=stop", shell=True, cwd=gofolder):
    while 0 != _gosubprocess("./ble-backend -command=nok_ident -maclist=stop"):
        # time.sleep(Timeout)
        # if loop==3:
        if loop==1:
            logger_app.error('==blink_stop failed==') 
            return -1
        loop+=1
    logger_app.info('==blink_stop success==')
    return 0

def turn_on_all():
    loop = 1
    while 0 != _gosubprocess("./ble-backend -command=allon"):
        # time.sleep(Timeout)
        if loop==1:
            logger_app.error('==turn_on_all failed==') 
            return -1
        loop+=1
    logger_app.info('==turn_on_all success==')
    return 0

def turn_off_all():
    loop = 1
    while 0 != _gosubprocess("./ble-backend -command=alloff"):
        # time.sleep(Timeout)
        if loop==1:
            logger_app.error('==turn_off_all failed==') 
            return -1
        loop+=1
    logger_app.info('==turn_off_all success==')
    return 0

def kickout_all():
    loop = 1
    while 0 != _gosubprocess("./ble-backend -command=allkickout"):
        # time.sleep(Timeout)
        if loop==1:
            logger_app.error('==kickout_all failed==') 
            return -1
        loop+=1
    logger_app.info('==kickout_all success==')
    return 0

def indicator_r():
    loop = 1
    while 0 != _gosubprocess("./ble-backend -command=indrgb -color=1"):
        # time.sleep(Timeout)
        if loop==1:
            logger_app.error('==indicator_r failed==') 
            return -1
        loop+=1
    logger_app.info('==indicator_r success==')
    return 0

def indicator_g():
    loop = 1
    while 0 != _gosubprocess("./ble-backend -command=indrgb -color=2"):
        # time.sleep(Timeout)
        if loop==1:
            logger_app.error('==indicator_g failed==') 
            return -1
        loop+=1
    logger_app.info('==indicator_g success==')
    return 0


def indicator_b():
    loop = 1
    while 0 != _gosubprocess("./ble-backend -command=indrgb -color=3"):
        # time.sleep(Timeout)
        if loop==1:
            logger_app.error('==indicator_b failed==') 
            return -1
        loop+=1
    logger_app.info('==indicator_b success==')
    return 0

# @processmaker
def blink_failed():

    filter_failed = {
        or_(
            Testdata.bool_qualified_signal == False,
            Testdata.bool_qualified_check == False,
            Testdata.bool_qualified_scan == False,
            Testdata.bool_qualified_deviceid == False,
            Testdata.reserve_bool_1 == False,
        )
    }
    datas_all = Testdata.query.all()
    datas_failed = Testdata.query.filter(*filter_failed).all()
    num_all = len(datas_all)
    num_failed = len(datas_failed)
    if num_all >= 1 and num_all == num_failed:
        logger_app.warn('==auto blink: {} of {} failed, blink all=='.format(num_failed, num_all))
        blink_all()
        return 0
    logger_app.info('==auto blink: {} of {} failed, blink every single failed one=='.format(num_failed, num_all))
    macs = list()
    for data in datas_failed:
        macs.append(data.mac_ble)
    # for mac in macs:
    #     blink_single(mac)
    blink_group(macs)
    return 0


######################
## legacy functions ##
######################

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

@threadmaker
def watch_log_legacy():
    logfile = os.path.join(logfolder, 'log_app.txt')
    p = subprocess.Popen("tail -f {}".format(logfile), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while get_running_state_sql():
        output = p.stdout.readline().decode('utf-8')[0:-1]
        socketio.emit('mylog', output, namespace='/test', broadcast=True)
    p.kill()

@threadmaker
def watch_to_jump_legacy():
    while True:
        if get_running_state_sql():
            # time.sleep(2)
            socketio.sleep(2)
        else:
            logger_app.info('==emit event_done==')
            socketio.emit('mydone', namespace='/test', broadcast=True)
            break

