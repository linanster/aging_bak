#! /usr/bin/env python3
# coding:utf8
#
from flask import Flask
from models import init_models
from views import init_views


app = Flask(__name__)
app.config['SECRET_KEY'] = "random string"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ge.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_models(app)
init_views(app)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True, threaded=True)
