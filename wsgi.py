# coding:utf8
#
from app import create_app
import sys

print('==sys.version==',sys.version)
print('==sys.executable==',sys.executable)

application_ge_aging = create_app()

@application_ge_aging.template_global('devicecode')
def devicecode():
    from app.lib import get_devicecode
    from app.models import Device
    code = get_devicecode()
    if code == 0:
        name = "未知"
    else:
        name = Device.query.filter_by(code=code).first().name
    return name

@application_ge_aging.template_global('totalcount')
def totalcount():
    from app.lib import get_totalcount
    return get_totalcount()

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

@application_ge_aging.template_filter('parse_status')
def parseStatusCode(code):
    if '2' in str(code):
        plaintxt = '失败'
    else:
        plaintxt = '成功'
    return '{}({})'.format(plaintxt,code)

@application_ge_aging.template_filter('parse_status_boolean')
def parseStatusCodeBoolean(code):
    if '2' in str(code):
        statusbool = False
    else:
        statusbool = True
    return statusbool
