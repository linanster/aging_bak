#! /usr/bin/env python2
# coding: utf8
#
import time
import os
import subprocess

def start():
    try:
        print 'starting...'
        time.sleep(3)
        # print os.getcwd() - /git/aging/flask
        p = subprocess.Popen("./ble-backend --scan", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=None)
        # 模拟错误
        # raise Error
    except Exception as e:
        print str(e)
        return 1
    else:
        print "start success"
        return 0
    
def stop():
    try:
        print "stopping..."
        os.system("ps aux | grep -v grep | grep ble-backend | awk '{print $2}' | xargs kill")
    except Exception as e:
        print str(e)
        return 1
    else:
        print "stop success"
        return 0
    
