from flask import Blueprint, request, render_template, flash, redirect, url_for

blue_index = Blueprint('blue_index', __name__)


@blue_index.route('/')
@blue_index.route('/index/')
def index():
    return render_template('index.html')
