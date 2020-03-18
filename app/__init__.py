#! /usr/bin/env python3
# coding:utf8
#
from flask import Flask
from .models import init_models
from .views import init_views
from .settings import config
from .ext import init_ext

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['nan1'])
    init_models(app)
    init_views(app)
    init_ext(app)
    return app

