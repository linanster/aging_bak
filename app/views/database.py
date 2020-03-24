from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
import datetime

from app.models import db, tb_device_type, tb_factory, tb_data_aging
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
    control_index = request.args.get('control_index')

    # pagination code
    PER_PAGE = 30
    page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    start = (page-1)*PER_PAGE
    end = page * PER_PAGE if len(results) > page * PER_PAGE else len(results)
    pagination = Pagination(page=page, total=len(results), per_page=PER_PAGE, bs_version=3)
    ret = view_data_aging.query.slice(start, end)

    return render_template('manageaging.html', pagination=pagination, results=ret, control_index=control_index)


@blue_database.route('/info_device/', methods=['GET'])
def info_device():
    results = tb_device_type.query.all()
    return render_template('managedevice.html', results=results)

@blue_database.route('/info_factory/', methods=['GET'])
def info_factory():
    results = tb_factory.query.all()
    return render_template('managefactory.html', results=results)




