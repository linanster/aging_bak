from threading import Lock
import os


topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
appfolder = os.path.abspath(os.path.join(topdir, "app"))
gofolder = os.path.abspath(os.path.join(topdir, "go"))
logfolder = os.path.abspath(os.path.join(topdir, "log"))
sqlitefolder = os.path.abspath(os.path.join(topdir, "app", "sqlite"))
upgradefolder = os.path.abspath(os.path.join(topdir, "upgrade"))


# days of keep archive data on local Rasp Pi
RETENTION = 7

# gecloud IP address
# gecloud_ip = '10.30.30.101'
gecloud_ip = '47.101.215.138'
