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

@manager.command
def uninit():
    from app.models import db
    db.drop_all(bind='sqlite')

@manager.option('--factory', dest="code")
def customize(code):
    from app.lib import set_factorycode
    set_factorycode(code)

@manager.command
def createdb():
    from app.models import db, Device, Factory
    from app.lib import create_view
    db.create_all(bind='mysql')
    create_view()
    Device.seed()
    Factory.seed()

@manager.command
def deletedb():
    from app.models import db
    from app.lib import delete_view
    delete_view()
    db.drop_all(bind='mysql')

@manager.command
def testdata():
    from app.models import Testdata
    Testdata.seed()

@app.template_global('running')
def running():
    from app.lib import get_running_state
    return get_running_state()

@app.template_global('paused')
def paused():
    from app.lib import get_paused_state
    return get_paused_state()

if __name__ == '__main__':
    manager.run()

