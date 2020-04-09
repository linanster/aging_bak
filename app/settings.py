import os

# 1.Global static variable definition

# called by models.tables.py
# called by manage.py init function
# 1 -- Leedarson
# 2 -- Innotech
# 3 -- Tonly
# 4 -- Changhong
FCODE=1

# called by lib.mycmd.py
Debug = True
# called by lib.mycmd.py
# timeout for go binary
Timeout = 5

topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
gofolder = os.path.abspath(os.path.join(topdir, "go"))
logfolder = os.path.abspath(os.path.join(topdir, "log"))
# 2. Flask app configuration

class Config():
    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = gofolder
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 4000
    
class NanConfig1(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/ge' 
    SQLALCHEMY_BINDS = {
    'mysql': 'mysql+pymysql://root:123456@localhost:3306/ge',
    'sqlite': 'sqlite:///sqlite/system.sqlite3'
    }


class NanConfig2(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ge.sqlite3'

config = {
    'nan1': NanConfig1,
    'nan2': NanConfig2
}

