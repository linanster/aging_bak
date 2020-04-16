from threading import Lock
import os

thread = None
thread_lock = Lock()


topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
appfolder = os.path.abspath(os.path.join(topdir, "app"))
gofolder = os.path.abspath(os.path.join(topdir, "go"))
logfolder = os.path.abspath(os.path.join(topdir, "log"))
sqlitefolder = os.path.abspath(os.path.join(topdir, "app", "sqlite"))
