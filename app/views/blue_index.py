from flask import Blueprint, redirect, url_for
from .blue_test import blue_test

blue_index = Blueprint('blue_index', __name__, url_prefix='/')

@blue_index.route('/')
@blue_index.route('/index')
@blue_index.route('/index/')
def vf_index():
    return redirect(url_for('blue_test.vf_start'))
