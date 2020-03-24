from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
import datetime

from app.models import db, tb_device_type, tb_factory, tb_data_aging
from app.models import view_data_aging

# create_view and delete_view is actually two pymysql execute function
# not that like typical models, such as db
from app.lib import create_view, delete_view

blue_manage = Blueprint('blue_manage', __name__, url_prefix='/manage')

# 1. view functions definition

@blue_manage.route('/data', methods=['GET'])
def vf_data():
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

    return render_template('manage_data.html', pagination=pagination, results=ret, control_index=control_index)


@blue_manage.route('/device', methods=['GET'])
def vf_device():
    results = tb_device_type.query.all()
    return render_template('manage_device.html', results=results)

@blue_manage.route('/factory', methods=['GET'])
def vf_factory():
    results = tb_factory.query.all()
    return render_template('manage_factory.html', results=results)




