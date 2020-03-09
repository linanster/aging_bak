#! /usr/bin/env python3
# coding: utf8
#
import time
import os
import subprocess

DEBUG = False
program = "./ble-backend-nan" if DEBUG else "./ble-backend"

def start():
    try:
        print('starting...')
        time.sleep(1)
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

def changemesh():
    try:
        # p = subprocess.Popen("./ble-backend-nan -command=changemesh", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        # p = subprocess.Popen("./ble-backend -command=changemesh", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        p = subprocess.Popen("{} -command=changemesh".format(program), shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
    except Exception as e:
        print("change mesh error:", str(e))
        return 1
    else:
        print("change mesh success")
        return 0
    
def scan():
    try:
        # p = subprocess.Popen("./ble-backend-nan -command=scan", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        # p = subprocess.Popen("./ble-backend -command=scan", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        p = subprocess.Popen("{} -command=scan".format(program), shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
    except Exception as e:
        print("scan error:", str(e))
        return 1
    else:
        print("scan success")
        return 0

def stop():
    try:
        print ("stopping...")
        os.system("ps aux | grep -v grep | grep ble-backend | awk '{print $2}' | xargs kill")
    except Exception as e:
        print(str(e))
        return 1
    else:
        print("stop success")
        return 0
    
