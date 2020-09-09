from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory, Response
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import text
import datetime
import os
import stat
from werkzeug.utils import secure_filename

from app.models import Device, Factory, TestdataStage, TestdataArchive
from app.lib.execmodel import testdatasarchive_cleanup

from app.lib import get_factorycode
from app.lib import viewfunclog, logger_app
from app.lib import gen_excel, empty_folder
from app.lib import exec_upgrade, check_github_connection
from app.lib.cloudhandler import upload_to_cloud

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
    elif fcode in (1, 2, 3, 4, 5, 6):
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
    # fcode = get_factorycode()
    # if fcode == 0:
    #     results = Device.query.all()
    # elif fcode in (1, 2, 3, 4, 5):
    #     # factory = Factory.query.filter(Factory.code.__eq__(fcode)).first()
    #     factory = Factory.query.filter(Factory.code == fcode).first()
    #     results = factory.devices
    # elif fcode in (6,):
    #     d_leedarson_128 = Device.query.filter(Device.code == 128).first()
    #     results = [d_leedarson_128, ]
    # else:
    #     results = list()
    results = Device.query.all()
    return render_template('manage_device.html', results=results)


########################
## manage data module ##
########################

@blue_manage.route('/data', methods=['GET', 'post'])
@viewfunclog
def vf_data():
    delete_count = request.args.get('delete_count')
    # 如果设备类型未选择，devicecode此时为None
    search_devicecode = request.form.get('devicecode', type=str)
    # 如果Ble Mac栏为空，blemac此时为“”。注意，不是None
    search_blemac = request.form.get('blemac', type=str)
    # if len(search_blemac) == 0:
    #     search_blemac = None

    myquery = TestdataArchive.query.filter(
        TestdataArchive.devicecode.like("%"+search_devicecode+"%") if search_devicecode is not None else text(""),
        TestdataArchive.mac_ble.like("%"+search_blemac+"%") if search_blemac is not None else text(""),
        )
    # datas = TestdataArchive.query.all()
    datas = myquery.all()

    total_count = len(datas)

    # pagination code
    PER_PAGE = 50
    page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    start = (page-1)*PER_PAGE
    end = page * PER_PAGE if total_count > page * PER_PAGE else total_count
    pagination = Pagination(page=page, total=total_count, per_page=PER_PAGE, bs_version=3)
    # ret = TestdataArchive.query.slice(start, end)
    ret = myquery.slice(start, end)
    return render_template('manage_data.html', pagination=pagination, results=ret, delete_count=delete_count, search_devicecode=search_devicecode, search_blemac=search_blemac)

@blue_manage.route('/cmd_deletearchive', methods=['POST'])
@viewfunclog
def cmd_deletearchive():
    count = testdatasarchive_cleanup()
    flash('删除了 {} 条数据'.format(count))
    return redirect(url_for('blue_manage.vf_data', delete_count = count))


@blue_manage.route('/cmd_download_testdatasarchive', methods=['POST'])
@viewfunclog
def cmd_download_testdatasarchive():
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    excelname = 'TestdatasArchive-' + timestamp + '.xls'
    excelfolder = os.path.join(topdir, 'pub','excel')
    filename = os.path.join(excelfolder, excelname)
    empty_folder(excelfolder)
    gen_excel(TestdataArchive, filename)
    # 普通下载
    # return send_from_directory(excelfolder, excelname, as_attachment=True)
    # 流式读取
    def send_file():
        with open(filename, 'rb') as filestream:
            while True:
                data = filestream.read(1024*1024) # 每次读取1M大小
                if not data:
                    break
                yield data
    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % excelname
    return response


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
    if errno is not None and errmsg is not None:
        logger_app.info("[upgrade] errno: {}".format(errno))
        logger_app.info("[upgrade] errmsg: {}".format(errmsg))
        # logger_app.info("[upgrade] network_enabled: {}".format(network_enabled))
        return render_template('manage_upgrade.html', upgrade_errno=errno, upgrade_errmsg=errmsg)
    elif network_enabled is not None:
        # logger_app.info("[upgrade] errno: {}".format(errno))
        # logger_app.info("[upgrade] errmsg: {}".format(errmsg))
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
        0: 'git pull 拉取代码成功',
        1: 'git pull 拉取代码错误',
        11: 'Github 网络连接错误',
        12: '升级验证码错误',
    }
    # call upgrade function
    errno = exec_upgrade(pin)
    errmsg = errtable.get(errno) 
    if errno == 0:
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


