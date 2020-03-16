from flask import Blueprint, request, render_template, flash, redirect, url_for
from app.models import view_data_aging, tb_data_aging



blue_nav = Blueprint('blue_nav', __name__)


@blue_nav.route('/')
@blue_nav.route('/index/')
def index():
    return render_template('index.html')

@blue_nav.route('/manage/', methods=['GET'])
def manage():
    return render_template('manage.html')


@blue_nav.route('/about/')
def about():
    return render_template('about.html')

