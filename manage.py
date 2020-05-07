# coding: utf8

import sys
from flask_script import Manager

from app import create_app

app = create_app()

manager = Manager(app)

@manager.command
def hello():
    print('Hello, Manager Command!')

@manager.command
def init():
    from app.models import db_sqlite, Systeminfo, RunningState
    db_sqlite.create_all(bind='sqlite')
    Systeminfo.seed()
    RunningState.seed()
    from app.lib import set_factorycode
    from app.fcode import FCODE
    set_factorycode(FCODE)

@manager.command
def uninit():
    from app.models import db_sqlite
    db_sqlite.drop_all(bind='sqlite')

@manager.command
def createdb():
    from app.models import db_mysql, Device, Factory
    db_mysql.create_all(bind='mysql')
    Factory.seed()
    Device.seed()

@manager.command
def deletedb():
    from app.models import db_mysql
    db_mysql.drop_all(bind='mysql')

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

