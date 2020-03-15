#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess
from multiprocessing import Process
from flask import flash, redirect, url_for
from .mypymysql import migrate_to_stage, migrate_to_archive, cleanup_temp, cleanup_stage

TEST = True
program = "./ble-backend-nan" if TEST else "./ble-backend"

gofolder = os.path.join(os.getcwd(), 'go')


def async_call(fn):
    def wrapper(*args, **kwargs):
        Process(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

@async_call
def start(pipe_recv, pipe_send):
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
        try:
            buf, = pipe_recv.recv(100)
            print('[debug] process start(scan) receive:', buf)
            if 'stop' == buf:
                break
            else:
                continue
        except:
            # move data to another place
            cleanup_temp()
            _scan()
            # todo: refresh page info_age with scan_loop
            time.sleep(10)
            # todo: cause table lock
            # migrate_to_stage()
    pipe_send.send('stopped')
    print('[debug] process start(scan) send: stopped')
    return 0

# @async_call
def stop(pipe_recv, pipe_send):
    pipe_send.send('stop')
    print('[debug] process stop send: stop')
    buf = pipe_recv.recv(10)
    print('[debug] process stop receive:', buf)
    if 'stopped' == buf:
        return 0
    else:
        return 1

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
def _scan():
    print('scan start...')
    p = subprocess.Popen("{} -command=scan".format(program), shell=True, cwd=gofolder)
    # p.wait()

    
