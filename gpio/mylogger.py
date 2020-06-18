import logging
from logging.handlers import RotatingFileHandler
import os

from myglobals import logfolder

formatter1 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# 1. logger property set up
logfile1 = os.path.abspath(os.path.join(logfolder, "log_api_caller.txt"))

filehandler1 = RotatingFileHandler(logfile1, maxBytes = 10*1024*1024, backupCount=3)
filehandler1.setLevel(logging.INFO)
filehandler1.setFormatter(formatter1)

consolehandler1 = logging.StreamHandler()
consolehandler1.setLevel(logging.INFO)
consolehandler1.setFormatter(formatter1)

# 2.1 logger init
logger_api_caller = logging.getLogger('api_caller')
logger_api_caller.setLevel(level = logging.INFO)
logger_api_caller.addHandler(filehandler1)
logger_api_caller.addHandler(consolehandler1)
