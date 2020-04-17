from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory
from flask_paginate import Pagination, get_page_parameter
import time
import datetime
import os

from app.models import Testdata
from app.lib import start, blink_single, blink_all, blink_stop
from app.lib import watch_to_jump, watch_log
from app.lib import set_factorycode, set_devicecode, set_totalcount, set_running_state
from app.lib import get_errno, get_running_state
from app.lib import testdatas_archive
from app.lib import viewfunclog
from app.lib import logger
from app.lib import gen_excel, empty_folder

from app.settings import topdir


blue_test = Blueprint('blue_test', __name__, url_prefix='/test')


@blue_test.route('/error')
@viewfunclog
def vf_error():
    errno = request.args.get('errno')
    return render_template('test_error.html', errno=errno)

@blue_test.route('/config')
@viewfunclog
def vf_config():
    return render_template('test_config.html')

@blue_test.route('/start')
@viewfunclog
def vf_start():
    return render_template('test_start.html')

@blue_test.route('/running')
@viewfunclog
def vf_running():
    watch_to_jump()
    watch_log()
    return render_template('test_running.html')

@blue_test.route('/finished')
@viewfunclog
def vf_finished():
    results = Testdata.query.all()
    control_index = request.args.get('control_index')
    # pagination code
    # PER_PAGE = 30
    # page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    # start = (page-1)*PER_PAGE
    # end = page * PER_PAGE if len(results) > page * PER_PAGE else len(results)
    # pagination = Pagination(page=page, total=len(results), per_page=PER_PAGE, bs_version=3)
    # ret = Testdata.query.slice(start, end)
    # return render_template('testing.html', pagination=pagination, results=ret)
    return render_template('test_finished.html', results=results, control_index=control_index)


# button & command

@blue_test.route('/cmd_start_legacy', methods=['POST'])
@viewfunclog
def vf_cmd_start_legacy():
    time.sleep(1)
    # errno saved at sqlite, instead of return value here.
    # errno = start()
    start()
    # wait a second for start initializing sqlite running states
    time.sleep(1)
    return redirect(url_for('blue_test.vf_running')) 


@blue_test.route('/cmd_start', methods=['POST'])
@viewfunclog
def vf_cmd_start():
    logger.warn('click start button')
    set_running_state()
    start()
    return redirect(url_for('blue_test.vf_running')) 


@blue_test.route('/cmd_saveconfig', methods=['POST'])
@viewfunclog
def vf_cmd_saveconfig():
    # devicecode = request.form.get('devicecode')
    # factorycode = request.form.get('factorycode')
    totalcount = request.form.get('totalcount')
    # set_factorycode(factorycode)
    # set_devicecode(devicecode) 
    set_totalcount(totalcount) 
    return redirect(url_for('blue_test.vf_start'))

@blue_test.route('/cmd_blink_single', methods=['POST'])
@viewfunclog
def vf_cmd_blink_single():
    logger.warn('click blink single button')
    mac = request.form.get('mac')
    index = request.form.get('index')
    blink_single(mac)
    return redirect(url_for('blue_test.vf_finished', control_index=index))

@blue_test.route('/cmd_blink_all', methods=['POST'])
@viewfunclog
def vf_cmd_blink_all():
    logger.warn('click blink all button')
    blink_all()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_blink_stop', methods=['POST'])
@viewfunclog
def vf_cmd_blink_stop():
    logger.warn('click blink stop button')
    blink_stop()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/process_finished')
@viewfunclog
def process_finished():
    running = get_running_state()
    if running:
        return redirect(url_for('blue_test.vf_running'))
    errno = get_errno()
    if errno == 0:
        testdatas_archive()
        return redirect(url_for('blue_test.vf_finished'))
    else:
        return redirect(url_for('blue_test.vf_error', errno=errno))

@blue_test.route('/cmd_download_testdatas', methods=['POST'])
@viewfunclog
def cmd_download_testdatas():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    excelname = 'Testdata-' + timestamp + '.xls'
    excelfolder = os.path.join(topdir, 'pub', 'excel')
    filename = os.path.join(excelfolder, excelname)
    empty_folder(excelfolder)    
    gen_excel(Testdata, filename)
    return send_from_directory(excelfolder, excelname, as_attachment=True)

