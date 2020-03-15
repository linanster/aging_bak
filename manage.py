
from flask_script import Manager

from app import create_app

app = create_app()

manager = Manager(app)

@manager.command
def hello():
    print('Hello, Manager Command!')

@manager.command
def deploy():
    pass

@manager.command
def undeploy():
    pass


if __name__ == '__main__':
    manager.run()

