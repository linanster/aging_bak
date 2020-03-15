
from flask_script import Manager

from app import create_app

app = create_app()

manager = Manager(app)

@manager.command
def hello():
    print('Hello, Manager Command!')

@manager.command
def createdb():
    from app.models import db, tb_device_type, tb_factory
    db.create_all()
    tb_device_type.seed()
    tb_factory.seed()

@manager.command
def deletedb():
    from app.models import db
    db.drop_all()

@manager.command
def testdata():
    from app.models import tb_data_aging
    tb_data_aging.seed()

@manager.command
def createview():
    from app.lib import create_view
    create_view()

@manager.command
def deleteview():
    from app.lib import delete_view
    delete_view()

if __name__ == '__main__':
    manager.run()

