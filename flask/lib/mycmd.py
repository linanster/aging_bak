#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess
from threading import Thread
from multiprocessing import Process
from flask import flash, redirect, url_for

DEBUG = True
program = "./ble-backend-nan" if DEBUG else "./ble-backend"

STOP = False
STOPPED = False

def async_call(fn):
    def wrapper(*args, **kwargs):
        # Thread(target=fn, args=args, kwargs=kwargs).start()
        Process(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

@async_call
def view_start(pipe1, pipe2):
    global STOP
    global STOPPED
    start()
    time.sleep(6)
    changemesh()
    time.sleep(3)
    while True:
        try:
            buf, = pipe2.recv(10)
            print('==pipe2.recv==', buf)
            if 'stop' == buf:
                break
        except:
            scan()
            time.sleep(10)
    pipe1.send('stopped')
    return 0

# @async_call
def view_stop(pipe1, pipe2):
    pipe2.send('stop')
    if pipe1.recv(10) == 'stopped': 
        return 0
    else:
        return 1
    # return redirect(url_for('handle_index'))

@async_call
def start():
    try:
        print('start start...')
        # print os.getcwd() - /git/aging/flask
        # p = subprocess.Popen("./ble-backend-nan --command=start", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        # p = subprocess.Popen("./ble-backend -command=start", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        p = subprocess.Popen("{} -command=start".format(program), shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
    except Exception as e:
        print("start error:",str(e))
        return 1
    else:
        print("start success")
        return 0

@async_call
def changemesh():
    try:
        print('changemesh start...')
        # p = subprocess.Popen("./ble-backend-nan -command=changemesh", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        # p = subprocess.Popen("./ble-backend -command=changemesh", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        p = subprocess.Popen("{} -command=changemesh".format(program), shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
    except Exception as e:
        print("change mesh error:", str(e))
        return 1
    else:
        print("change mesh success")
        return 0
    
@async_call
def scan():
    try:
        print('scan start...')
        # p = subprocess.Popen("./ble-backend-nan -command=scan", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        # p = subprocess.Popen("./ble-backend -command=scan", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        p = subprocess.Popen("{} -command=scan".format(program), shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
    except Exception as e:
        print("scan error:", str(e))
        return 1
    else:
        print("scan success")
        return 0

