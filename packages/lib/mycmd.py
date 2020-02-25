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
        # p = subprocess.Popen("/test/aging/packages/scan.py", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p = subprocess.Popen("/test/aging/packages/ble-backend --scan", shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
        # os.system("ps aux | grep -v grep | grep scan | awk '{print $2}' | xargs kill")
        os.system("ps aux | grep -v grep | grep ble-backend | awk '{print $2}' | xargs kill")
    except Exception as e:
        print str(e)
        return 1
    else:
        print "stop success"
        return 0
    
