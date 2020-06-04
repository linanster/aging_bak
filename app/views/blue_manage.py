from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory
from flask_paginate import Pagination, get_page_parameter
import datetime
import os
import stat
from werkzeug.utils import secure_filename

from app.models import Device, Factory, TestdataArchive
from app.lib.execmodel import testdatasarchive_cleanup

from app.lib import get_factorycode
from app.lib import viewfunclog, logger_app
from app.lib import gen_excel, empty_folder
from app.lib import exec_upgrade, check_github_connection

from app.myglobals import logfolder, gofolder, topdir

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
        # factory = Factory.query.get(fcode)
        factory = Factory.query.filter(Factory.code.__eq__(fcode)).first()
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

@blue_manage.route('/log/delete', methods=['GET'])
@viewfunclog
def cmd_delete_log():
    filename = request.args.get('filename')
    sourcefile = os.path.join(logfolder, filename)
    os.remove(sourcefile)
    return redirect(url_for('blue_manage.vf_log'))


###############
## go module ##
###############

@blue_manage.route('/go')
@viewfunclog
def vf_go():
    invisibles = ['.keep', '.gitkeep']
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
        # os.chmod(destfile, stat.S_IROTH)
        os.chmod(destfile, 0o777)
        flash('文件导入成功!')
    return redirect(url_for('blue_manage.vf_go'))

####################
## upgrade module ##
####################

@blue_manage.route('/upgrade')
@viewfunclog
def vf_upgrade():
    errno = request.args.get('errno', type=int)
    errmsg = request.args.get('errmsg', type=str)
    network_enabled = request.args.get('network_enabled', type=int)
    if errno is not None:
        logger_app.info("[upgrade] errno: {}".format(errno))
        logger_app.info("[upgrade] errmsg: {}".format(errmsg))
        logger_app.info("[upgrade] network_enabled: {}".format(network_enabled))
        return render_template('manage_upgrade.html', upgrade_errno=errno, upgrade_errmsg=errmsg)
    elif network_enabled is not None:
        logger_app.info("[upgrade] errno: {}".format(errno))
        logger_app.info("[upgrade] errmsg: {}".format(errmsg))
        logger_app.info("[upgrade] network_enabled: {}".format(network_enabled))
        return render_template('manage_upgrade.html', network_enabled=network_enabled)
    else:
        return render_template('manage_upgrade.html')
        

@blue_manage.route('/upgrade/execute', methods=['POST'])
@viewfunclog
def cmd_upgrade():
    logger_app.info('[upgrade] click upgrade button')
    pin = request.form.get('pin', type=str)
    errtable = {
        0: 'success',
        1: 'pull upgrade error',
        2: 'restart service error',
        3: 'check service status error',
        11: 'network error',
        12: 'upgrade auth code error',
        -15: 'service restarted'
    }
    # call upgrade function
    errno = exec_upgrade(pin)
    errmsg = errtable.get(errno) 
    if errno in [0, -15]:
        flash('升级成功({0}):{1}'.format(errno,errmsg))
    else:
        flash('升级失败({0}):{1}'.format(errno,errmsg))
        
    params = {'errno':errno, 'errmsg':errmsg}
    return redirect(url_for('blue_manage.vf_upgrade', **params))

@blue_manage.route('/upgrade/checknetwork', methods=['POST'])
@viewfunclog
def cmd_checknetwork():
    logger_app.info('[upgrade] click check network button')
    if check_github_connection():
        network_enabled = 1
        flash('网络可用!')
    else:
        network_enabled = 0
        flash('网络不可用，请检查是否可连接至github.com!')
    return redirect(url_for('blue_manage.vf_upgrade', network_enabled=network_enabled))


