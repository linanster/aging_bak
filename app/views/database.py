from flask import Blueprint, request, render_template, flash, redirect, url_for
import datetime

from app.models import db, db_stage, db_archive, tb_device_type, tb_factory, tb_data_aging
from app.models import view_data_aging

# create_view and delete_view is actually two pymysql execute function
# not that like typical models, such as db
from app.lib import create_view, delete_view

blue_database = Blueprint('blue_database', __name__)

# 1. view functions definition

@blue_database.route('/info_aging/', methods=['GET'])
def info_aging():
    # results = tb_data_aging.query.all()
    results = view_data_aging.query.all()
    refresh = request.args.get('refresh')
    # print('==refresh==:', refresh)
    if refresh:
        return render_template('db_query_aging.html', results=results, refresh=True)
    return render_template('db_query_aging.html', results=results)


@blue_database.route('/info_device/', methods=['GET'])
def info_device():
    results = tb_device_type.query.all()
    return render_template('db_query_device.html', results=results)

@blue_database.route('/info_factory/', methods=['GET'])
def info_factory():
    results = tb_factory.query.all()
    return render_template('db_query_factory.html', results=results)

  



