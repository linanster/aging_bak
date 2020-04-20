from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory
from flask_paginate import Pagination, get_page_parameter
import datetime
import os
import stat
from werkzeug.utils import secure_filename

from app.models import db, Device, Factory, TestdataArchive
from app.lib import testdatasarchive_cleanup

from app.lib import get_factorycode
from app.lib import viewfunclog
from app.lib import gen_excel, empty_folder

from app.settings import logfolder
from app.settings import gofolder

from app.settings import topdir

blue_manage = Blueprint('blue_manage', __name__, url_prefix='/manage')


###########################
## manage factory module ##
###########################

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


##########################
## manage device module ##
##########################

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


########################
## manage data module ##
########################

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

@blue_manage.route('/cmd_deletearchive', methods=['POST'])
@viewfunclog
def cmd_deletearchive():
    testdatasarchive_cleanup()
    return redirect(url_for('blue_manage.vf_data'))

@blue_manage.route('/cmd_download_testdatasarchive', methods=['POST'])
@viewfunclog
def cmd_download_testdatasarchive():
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    excelname = 'TestdatasArchive-' + timestamp + '.xls'
    excelfolder = os.path.join(topdir, 'pub','excel')
    filename = os.path.join(excelfolder, excelname)
    empty_folder(excelfolder)
    gen_excel(TestdataArchive, filename)
    return send_from_directory(excelfolder, excelname, as_attachment=True)

################
## log module ##
################

@blue_manage.route('/log')
@viewfunclog
def vf_log():
    invisibles = ['.keep', '.gitkeep']
    filelist = os.listdir(logfolder)
    for f in invisibles:
        if f in filelist:
            filelist.remove(f)
        else:
            continue
    return render_template('manage_log.html', filelist=filelist)

@blue_manage.route('/log/view', methods=['GET'])
@viewfunclog
def cmd_view_log():
    filename = request.args.get('filename')
    return send_from_directory(logfolder, filename, as_attachment=False)

@blue_manage.route('/log/download', methods=['GET'])
@viewfunclog
def cmd_download_log():
    filename = request.args.get('filename')
    return send_from_directory(logfolder, filename, as_attachment=True)


###############
## go module ##
###############

@blue_manage.route('/go')
@viewfunclog
def vf_go():
    invisibles = ['.keep', '.gitkeep', 'ble-backend-nan', 'ble-backend.bak', 'config.json.bak']
    filelist = os.listdir(gofolder)
    for filename in invisibles:
        if filename in filelist:
            filelist.remove(filename)
        else:
            continue
    return render_template('manage_go.html', filelist=filelist)

@blue_manage.route('/go/download', methods=['GET'])
@viewfunclog
def cmd_download_go():
    filename = request.args.get('filename')
    return send_from_directory(gofolder, filename, as_attachment=True)


@blue_manage.route('/go/view', methods=['GET'])
@viewfunclog
def cmd_view_go():
    filename = request.args.get('filename')
    return send_from_directory(gofolder, filename, as_attachment=False)

@blue_manage.route('/go/delete', methods=['GET'])
@viewfunclog
def cmd_delete_go():
    filename = request.args.get('filename')
    sourcefile = os.path.join(gofolder, filename)
    os.remove(sourcefile)
    return redirect(url_for('blue_manage.vf_go'))

@blue_manage.route('/go/upload', methods=['POST'])
@viewfunclog
def cmd_upload_go():
    file = request.files['file']
    if file.filename == '':
        flash('请选择文件!')
    if file:
        filename = secure_filename(file.filename)            
        # filename = 'config.json'
        destfile = os.path.join(gofolder, filename)
        file.save(destfile)
        os.chmod(destfile, stat.S_IROTH)
        flash('文件导入成功!')
    return redirect(url_for('blue_manage.vf_go'))

####################
## upgrade module ##
####################

@blue_manage.route('/upgrade')
@viewfunclog
def vf_upgrade():
    return render_template('manage_upgrade.html')
