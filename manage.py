# coding: utf8

import sys
from flask_script import Manager

from app import create_app
from app.models.mysql import db_mysql, Device, Factory, Testdata, TestdataStage, TestdataArchive
from app.models.sqlite import db_sqlite, Systeminfo, RunningState

app = create_app()

manager = Manager(app)

@manager.command
def hello():
    print('Hello, Manager Command!')

@manager.command
def createdb_sqlite(table=False, data=False):
    from app.lib import set_factorycode
    from app.fcode import FCODE
    if table:
        db_sqlite.create_all(bind='sqlite')
        print('==create sqlite tables==')
    if data:
        Systeminfo.seed()
        RunningState.seed()
        set_factorycode(FCODE)
        print('==initialize sqlite datas==')

@manager.command
def deletedb_sqlite(table=False, data=False):
    if table:
        db_sqlite.drop_all(bind='sqlite')
        print('==delete sqlite tables==')
        return
    if data:
        Systeminfo.query.delete()
        RunningState.query.delete()
        db_sqlite.session.commit()
        print('==delete sqlite datas==')

@manager.command
def createdb_mysql(table=False, data=False):
    if table:
        db_mysql.create_all(bind='mysql')
        print('==create mysql tables==')
    if data:
        Factory.seed()
        Device.seed()
        print('==initialize mysql datas==')

@manager.command
def deletedb_mysql(table=False, data=False):
    if table:
        db_mysql.drop_all(bind='mysql')
        print('==delete mysql tables==')
        return
    if data:
        TestdataArchive.query.delete()
        TestdataStage.query.delete()
        Testdata.query.delete()
        Device.query.delete()
        Factory.query.delete()
        db_mysql.session.commit()
        print('==delete mysql datas==')

@manager.command
def cleanup(db=False, log=False, pycache=False, all=False):
    from app.lib.execsql import sql_testdatas_cleanup, sql_testdatasstage_cleanup, sql_testdatasarchive_cleanup
    from app.lib.myutils import cleanup_log, cleanup_pycache
    if all or db:
        print('==cleanup database==')
        sql_testdatas_cleanup()
        sql_testdatasstage_cleanup()
        sql_testdatasarchive_cleanup()
    if all or log:
        print('==cleanup log==')
        cleanup_log()
    if all or pycache:
        print('==cleanup pycache==')
        cleanup_pycache()

@manager.command
def updatefcode():
    from app.lib import set_factorycode, get_factorycode
    from app.fcode import FCODE
    set_factorycode(FCODE)
    print(get_factorycode())


@manager.option('--fcode', dest="code")
def setfcode(code):
    from app.lib import set_factorycode
    set_factorycode(code)

@manager.command
def getfcode():
    from app.lib import get_factorycode
    print(get_factorycode())

@manager.command
def upload():
    from app.lib import upload_to_cloud
    return upload_to_cloud()

@manager.command
def purge():
    from app.lib import purge_local_archive
    return purge_local_archive()


@app.template_global('devicename')
def devicename():
    from app.lib import get_devicename
    return get_devicename()

@app.template_global('devicecode')
def devicecode():
    from app.lib import get_devicecode
    return get_devicecode()

@app.template_global('totalcount')
def totalcount():
    from app.lib import get_totalcount
    return get_totalcount()

@app.template_global('fwversion')
def fwversion():
    from app.lib import get_fwversion
    return get_fwversion()

@app.template_global('mcuversion')
def mcuversion():
    from app.lib import get_mcuversion
    return get_mcuversion()

@app.template_global('progress')
def progress():
    from app.lib import get_progress
    return get_progress()

@app.template_global('running')
def running():
    from app.lib import get_running_state
    return get_running_state()

@app.template_global('phase')
def phase():
    from app.lib import get_phase
    return get_phase()

@app.template_global('errno')
def errno():
    from app.lib import get_errno
    return get_errno()

@app.template_filter('parse_is_qualified')
def parseIsQualified(mybool):
    return '成功' if mybool else '失败'

@app.template_filter('parse_rssi_wifi_na')
def parseRssiWifiNa(rssiwifi):
    if rssiwifi == 1:
        return 'na'
    else:
        return rssiwifi



if __name__ == '__main__':
    manager.run()

