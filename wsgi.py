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

@application_ge_aging.template_global('wifi_mac_low')
def wifi_mac_low():
    from app.lib.tools import get_sqlite_value3
    return get_sqlite_value3('r_wifi_mac_low')
@application_ge_aging.template_global('wifi_mac_high')
def wifi_mac_high():
    from app.lib.tools import get_sqlite_value3
    return get_sqlite_value3('r_wifi_mac_high')
@application_ge_aging.template_global('ble_mac_low')
def ble_mac_low():
    from app.lib.tools import get_sqlite_value3
    return get_sqlite_value3('r_ble_mac_low')
@application_ge_aging.template_global('ble_mac_high')
def ble_mac_high():
    from app.lib.tools import get_sqlite_value3
    return get_sqlite_value3('r_ble_mac_high')

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

@application_ge_aging.template_global('errinfo')
def errinfo():
    from app.lib import get_errno
    errno = get_errno()
    errtab = {
        1: '1: gotool or config.json file doesn’t exist or their size is zero, please check files in /root/aging/go',
        2: '2: ble connection failure, sometime you need to restart Raspberry',
        3: '3: no device can be found, you should power off/on devices, or restart Raspberry',
        4: '4: Database failure, it is one very rare error',
        5: '5: test is running, you click button too quick, so your command can’t run',
        6: '6: dialing timeout, usually you need to restart Raspberry',
        7: '7: command timeout,  maybe you should restart Raspberry',
        8: '8:  Session Key is empty, this ble connection is invalid',
        11: '11: required params is not set',
    }
    return errtab.get(errno, 'unknown error')

@application_ge_aging.template_global('gecloud_online_status')
def gecloud_online_status():
    from app.lib.tools import get_gecloud_online
    if get_gecloud_online():
        return '在线'
    else:
        return '离线'

@application_ge_aging.template_filter('parse_is_qualified')
def parseIsQualified(mybool):
    return '成功' if mybool else '失败'

@application_ge_aging.template_filter('parse_mac_is_qualified')
def parseMacIsQualified(res):
    if res == 0:
        return '成功'
    else:
        return '失败'

@application_ge_aging.template_filter('parse_rssi_wifi_na')
def parseRssiWifiNa(rssiwifi):
    if rssiwifi == 1:
        return 'na'
    else:
        return rssiwifi
