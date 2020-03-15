#! /usr/bin/env python3
# coding:utf8
#
from flask import Flask
from .models import init_models
from .views import init_views
from .settings import config
from .ext import init_bootstrap, init_nav

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['nan1'])
    init_models(app)
    init_views(app)
    init_bootstrap(app)
    init_nav(app)
    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True)
