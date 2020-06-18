# coding:utf8
#
import requests
import sys

from mylogger import logger_api_caller
from mydecorator import apicalllog

rasp_ip = 'localhost'
rasp_port = '5000'

usage = '''Usage: %s [starttest] [allkickout]''' % (sys.argv[0])

@apicalllog
def call_rasp_api_type1(url):
    payload = {}
    headers= {}
    response = requests.request("POST", url, headers=headers, data = payload, timeout=300)
    return response

@apicalllog
def call_rasp_api_type2(url):
    pass


if __name__ == '__main__':

    try:
        cmd = sys.argv[1]
    except Exception as e:
        logger_api_caller.error(str(e))
        print(usage)
        sys.exit(10)

    try:
        if cmd in ['starttest', 'allkickout']:
            url = "http://{}:{}/api/cmd/{}".format(rasp_ip, rasp_port, cmd)
            response = call_rasp_api_type1(url)
            errno = response.json().get('errno')
            sys.exit(errno)
        else:
            logger_api_caller.warn("api [%s] is not supported" % cmd )
            print(usage)
            sys.exit(12)

    except Exception as e:
        logger_api_caller.error(str(e))
        sys.exit(11)
