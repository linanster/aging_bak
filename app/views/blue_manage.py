from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory
from flask_paginate import Pagination, get_page_parameter
import datetime
import os
import stat

from app.models import db, Device, Factory, TestdataArchive
from app.lib import testdatasarchive_cleanup

from app.lib import get_factorycode
from app.lib import viewfunclog
from app.settings import logfolder
from app.settings import gofolder

blue_manage = Blueprint('blue_manage', __name__, url_prefix='/manage')


# 1. view functions definition

@blue_manage.route('/factory', methods=['GET'])
@viewfunclog
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
@viewfunclog
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
@viewfunclog
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

@blue_manage.route('/log')
@viewfunclog
def vf_log():
    invisibles = ['.keep',]
    filelist = os.listdir(logfolder)
    for f in invisibles:
        if f in filelist:
            filelist.remove(f)
        else:
            continue
    return render_template('manage_log.html', filelist=filelist)

@blue_manage.route('/upgrade')
@viewfunclog
def vf_upgrade():
    return render_template('manage_upgrade.html')

@blue_manage.route('/cmd_deletearchive', methods=['POST'])
@viewfunclog
def cmd_deletearchive():
    testdatasarchive_cleanup()
    return redirect(url_for('blue_manage.vf_data'))

@blue_manage.route('/view')
@viewfunclog
def cmd_view():
    filename = request.args.get('filename')
    return send_from_directory(logfolder, filename, as_attachment=False)

@blue_manage.route('/download')
@viewfunclog
def cmd_download():
    filename = request.args.get('filename')
    return send_from_directory(logfolder, filename, as_attachment=True)

@blue_manage.route('/upload', methods=['POST'])
@viewfunclog
def cmd_upload():
    file = request.files['file']
    if file.filename == '':
        flash('请选择文件!')
    if file:
        # filename = secure_filename(file.filename)            
        filename = 'ble-backend'
        destfile = os.path.join(gofolder, filename)
        file.save(destfile)
        os.chmod(destfile, stat.S_IXOTH)
        flash('文件导入成功，升级完成!')
    return redirect(url_for('blue_manage.vf_upgrade'))

