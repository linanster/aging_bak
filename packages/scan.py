#! /usr/bin/env python2
# coding:utf8
#
import time
import os

while True:
    os.system('/test/aging/packages/ble-backend --scan')
    print "scan 10s"
    time.sleep(10)
