import requests
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import subprocess
import os

from .mylogger import logger_app

from app.myglobal import topdir, upgradefolder

disable_warnings(InsecureRequestWarning)


def check_github_connection():
    method = 'GET'
    ############################################
    url = "https://github.com"
    ############################################
    headers = {}
    payload = {}
    try:
        response = requests.request(method=method, url=url, headers=headers, data=payload, timeout=10, verify=False)
    except Exception as e:
        print(str(e))
        return False
    else:
        if response.ok:
            return True
        else:
            return False


def check_upgrade_pin(pin):
    pinfile = os.path.join(upgradefolder, 'pin.txt')
    pin_auth = open(pinfile).readline()
    pin_auth = pin_auth.replace('\r', '').replace('\n','')
    print('==pin==',pin)
    print('==pin_auth==',pin_auth)
    if pin == pin_auth:
        return True
    else:
        return False


def exec_upgrade(pin):
    # 1. check github available or not
    if not check_github_connection():
        return 11

    # 2. check upgrade authentication code
    if not check_upgrade_pin(pin):
        return 12

    # 3. start upgrade
    p = subprocess.Popen("./run.sh --upgrade", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=topdir)
    while p.poll() is None:
        output = p.stdout.readline().decode('utf-8')[0:-1]
        logger_app.info('[upgrade] {}'.format(output))
    errno = p.poll()
    if errno != 0:
        errmsg = p.stderr.read().decode('utf-8')[:-1]
        logger_app.error('[upgrade] {}'.format(errmsg))
        logger_app.error('[upgrade] errno:{}'.format(errno))
    p.stdout.close()
    p.stderr.close()
    return errno
