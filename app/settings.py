import os


class Config():
    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 4000
    
class NanConfig1(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/ge' 


class NanConfig2(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ge.sqlite3'

config = {
    'nan1': NanConfig1,
    'nan2': NanConfig2
}

