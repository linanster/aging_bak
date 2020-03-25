from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
import datetime

from app.models import db, Device, Factory, Testdata
from app.models import TestdataView

# create_view and delete_view is actually two pymysql execute function
# not that like typical models, such as db
from app.lib import create_view, delete_view

blue_manage = Blueprint('blue_manage', __name__, url_prefix='/manage')

# 1. view functions definition

@blue_manage.route('/data', methods=['GET'])
def vf_data():
    # results = Testdata.query.all()
    results = TestdataView.query.all()
    control_index = request.args.get('control_index')

    # pagination code
    PER_PAGE = 30
    page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    start = (page-1)*PER_PAGE
    end = page * PER_PAGE if len(results) > page * PER_PAGE else len(results)
    pagination = Pagination(page=page, total=len(results), per_page=PER_PAGE, bs_version=3)
    ret = TestdataView.query.slice(start, end)

    return render_template('manage_data.html', pagination=pagination, results=ret, control_index=control_index)


@blue_manage.route('/device', methods=['GET'])
def vf_device():
    results = Device.query.all()
    return render_template('manage_device.html', results=results)

@blue_manage.route('/factory', methods=['GET'])
def vf_factory():
    results = Factory.query.all()
    return render_template('manage_factory.html', results=results)




