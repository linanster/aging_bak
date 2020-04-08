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
    from app.models import db, Systeminfo, RunningState
    db.create_all(bind='sqlite')
    Systeminfo.seed()
    RunningState.seed()
    from app.lib import set_factorycode
    from app.settings import FCODE
    set_factorycode(FCODE)

@manager.command
def uninit():
    from app.models import db
    db.drop_all(bind='sqlite')

@manager.command
def createdb():
    from app.models import db, Device, Factory
    db.create_all(bind='mysql')
    Factory.seed()
    Device.seed()

@manager.command
def deletedb():
    from app.models import db
    db.drop_all(bind='mysql')

@manager.command
def testdata():
    from app.models import Testdata
    Testdata.seed()

@manager.option('--fcode', dest="code")
def set(code):
    from app.lib import set_factorycode
    set_factorycode(code)


if __name__ == '__main__':
    manager.run()

