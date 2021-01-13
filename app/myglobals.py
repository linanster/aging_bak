from threading import Lock
import os
from multiprocessing import Queue

# MIMIC = True
MIMIC = False

topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
appfolder = os.path.abspath(os.path.join(topdir, "app"))
gofolder = os.path.abspath(os.path.join(topdir, "go"))
logfolder = os.path.abspath(os.path.join(topdir, "logs"))
sqlitefolder = os.path.abspath(os.path.join(topdir, "sqlite"))
upgradefolder = os.path.abspath(os.path.join(topdir, "upgrade"))


# days of keep archive data on local Rasp Pi
RETENTION = 7

if MIMIC:
    gecloud_ip = '10.30.30.101'
    gecloud_port = 5100
    gecloud_protocol = 'http'
else:
    gecloud_ip = 'api.gelightingsh.com'
    # gecloud_port = 8443
    # gecloud_protocol = 'https'
    gecloud_port = 5100
    gecloud_protocol = 'http'



# called by lib.mycmd.py
Debug = True
# called by lib.mycmd.py
# timeout for go binary
Timeout = 5

# called by wsgi.py/count_stage_exceed()
MAX_UNUPLOAD_ALLOWED = 15000

# called by wsgi.py/count_archive_exceed()
# MAX_ARCHIVED_ALLOWED = 300
MAX_ARCHIVED_ALLOWED = 65000
