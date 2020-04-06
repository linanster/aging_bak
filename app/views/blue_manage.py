from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
import datetime

from app.models import db, Device, Factory, TestdataArchive
from app.lib import testdatasarchive_cleanup

from app.lib import get_factorycode

blue_manage = Blueprint('blue_manage', __name__, url_prefix='/manage')

# 1. view functions definition

@blue_manage.route('/factory', methods=['GET'])
def vf_factory():
    fcode = get_factorycode() 
    if fcode == 0:
        results = Factory.query.all()
    elif fcode in (1, 2, 3, 4, 5):
        # results = Factory.query.filter_by(code=fcode).first()
        result = Factory.query.filter_by(code=fcode).first()
        results = [result,]
    else:
        results = list()
    return render_template('manage_factory.html', results=results)

@blue_manage.route('/device', methods=['GET'])
def vf_device():
    fcode = get_factorycode() 
    if fcode == 0:
        results = Device.query.all()
    elif fcode in (1, 2, 3, 4, 5):
        # results = Device.query.filter_by(factorycode=fcode).all()
        # results = Device.query.filter_by(factorycode=fcode).all()
        factory = Factory.query.get(fcode)
        results = factory.devices
    else:
        results = list()
    return render_template('manage_device.html', results=results)

@blue_manage.route('/data', methods=['GET'])
def vf_data():
    results = TestdataArchive.query.all()

    # pagination code
    PER_PAGE = 50
    page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    start = (page-1)*PER_PAGE
    end = page * PER_PAGE if len(results) > page * PER_PAGE else len(results)
    pagination = Pagination(page=page, total=len(results), per_page=PER_PAGE, bs_version=3)
    ret = TestdataArchive.query.slice(start, end)

    return render_template('manage_data.html', pagination=pagination, results=ret)

@blue_manage.route('/cmd_deletearchive', methods=['POST'])
def cmd_deletearchive():
    testdatasarchive_cleanup()
    return redirect(url_for('blue_manage.vf_data'))


