#! /usr/bin/env python3
# coding:utf8
#
from flask import Flask
from models import init_models
from views import init_views
from settings import config


app = Flask(__name__)

app.config.from_object(config['nan1'])

init_models(app)
init_views(app)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True)
