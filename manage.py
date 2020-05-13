# coding: utf8

import sys
from flask_script import Manager

from app import create_app
from app.models.mysql import db_mysql, Device, Factory, Testdata, TestdataArchive
from app.models.sqlite import db_sqlite, Systeminfo, RunningState

app = create_app()

manager = Manager(app)

@manager.command
def hello():
    print('Hello, Manager Command!')

@manager.command
def createdb_sqlite(init=False):
    from app.lib import set_factorycode
    from app.fcode import FCODE
    if init:
        Systeminfo.seed()
        RunningState.seed()
        set_factorycode(FCODE)
    else:
        db_sqlite.create_all(bind='sqlite')

@manager.command
def deletedb_sqlite(uninit=False):
    if uninit:
       Systeminfo.query.delete()
       RunningState.query.delete()
       db_sqlite.session.commit()
    else:
        db_sqlite.drop_all(bind='sqlite')

@manager.command
def createdb_mysql(init=False):
    if init:
        Factory.seed()
        Device.seed()
    else:
        db_mysql.create_all(bind='mysql')

@manager.command
def deletedb_mysql(uninit=False):
    if uninit:
        TestdataArchive.query.delete()
        Testdata.query.delete()
        Device.query.delete()
        Factory.query.delete()
        db_mysql.session.commit()
    else:
        db_mysql.drop_all(bind='mysql')

@manager.command
def updatefcode():
    from app.lib import set_factorycode
    from app.fcode import FCODE
    set_factorycode(FCODE)


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


if __name__ == '__main__':
    manager.run()

