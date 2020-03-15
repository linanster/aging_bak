from flask import Blueprint, request, render_template, flash, redirect, url_for
from app.models import view_data_aging, tb_data_aging



blue_index = Blueprint('blue_index', __name__)


@blue_index.route('/')
@blue_index.route('/index/')
def index():
    return render_template('index.html')

@blue_index.route('/manage/', methods=['GET'])
def manage():
    return render_template('manage.html')


@blue_index.route('/about/')
def about():
    return render_template('about.html')

@blue_index.route('/testing/')
def testing():
    # results = tb_data_aging.query.all()
    results = view_data_aging.query.all()
    refresh = request.args.get('refresh')
    if refresh:
        return render_template('testing.html', results=results, refresh=True)
    return render_template('testing.html', results=results)

