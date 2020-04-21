import requests
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import subprocess

from app.myglobal import topdir

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



def check_upgrade_pin():
    pass

def exec_upgrade():
    errno = subprocess.call("./run.sh --upgrade", shell=True, cwd=topdir)
    return errno
