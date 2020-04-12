from multiprocessing import Process
from threading import Thread, Lock
from functools import wraps
from flask import request

from app.myglobal import thread, thread_lock
from .mylogger import logger

def processmaker(func):
    def inner(*args, **kwargs):
        Process(target=func, args=args, kwargs=kwargs).start()
    return inner

def threadmaker(func):
    def inner(*args, **kwargs):
        global thread
        with thread_lock:
            if thread is None:
                thread = Thread(target=func, args=args, kwargs=kwargs).start()
    return inner

def threadmaker_legacy(func):
    def inner(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
    return inner


def viewfunclog(func):
    @wraps(func)
    def inner(*args, **kargs):
        logger.info('{} {}'.format(request.method, request.url))
        return func(*args, **kargs)
    return inner

