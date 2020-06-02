# coding:utf8
#
from app import create_app
import sys

print('==sys.version==',sys.version)
print('==sys.executable==',sys.executable)

application_ge_aging = create_app()

@application_ge_aging.template_global('devicename')
def devicename():
    from app.lib import get_devicename
    return get_devicename()

@application_ge_aging.template_global('devicecode')
def devicecode():
    from app.lib import get_devicecode
    return get_devicecode()

@application_ge_aging.template_global('totalcount')
def totalcount():
    from app.lib import get_totalcount
    return get_totalcount()

@application_ge_aging.template_global('fwversion')
def fwversion():
    from app.lib import get_fwversion
    return get_fwversion()

@application_ge_aging.template_global('mcuversion')
def mcuversion():
    from app.lib import get_mcuversion
    return get_mcuversion()

@application_ge_aging.template_global('ble_strength_low')
def ble_strength_low():
    from app.lib import get_ble_strength_low
    return get_ble_strength_low()

@application_ge_aging.template_global('wifi_strength_low')
def wifi_strength_low():
    from app.lib import get_wifi_strength_low
    return get_wifi_strength_low()

@application_ge_aging.template_global('progress')
def progress():
    from app.lib import get_progress
    return get_progress()

@application_ge_aging.template_global('running')
def running():
    from app.lib import get_running_state
    return get_running_state()

@application_ge_aging.template_global('phase')
def phase():
    from app.lib import get_phase
    return get_phase()

@application_ge_aging.template_global('errno')
def errno():
    from app.lib import get_errno
    return get_errno()

@application_ge_aging.template_filter('parse_is_qualified')
def parseIsQualified(mybool):
    return '成功' if mybool else '失败'

@application_ge_aging.template_filter('parse_rssi_wifi_na')
def parseRssiWifiNa(rssiwifi):
    if rssiwifi == 1:
        return 'na'
    else:
        return rssiwifi
