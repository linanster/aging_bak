# coding: utf8

from flask_script import Manager

from app import create_app

app = create_app()

manager = Manager(app)

@manager.command
def hello():
    print('Hello, Manager Command!')

@manager.command
def createdb():
    from app.models import db, tb_device_type, tb_factory, tb_state
    db.create_all(bind='main')
    db.create_all(bind='state')
    tb_device_type.seed()
    tb_factory.seed()
    tb_state.seed()

@manager.command
def deletedb():
    from app.models import db
    db.drop_all()

@manager.command
def createview():
    from app.lib import create_view
    create_view()

@manager.command
def deleteview():
    from app.lib import delete_view
    delete_view()

@manager.command
def testdata():
    from app.models import tb_data_aging
    tb_data_aging.seed()

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

