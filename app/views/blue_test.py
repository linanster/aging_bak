from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
import time

from app.models import TestdataView, Testdata
from app.lib import start, blink_single, blink_all, blink_stop
from app.lib import watch_to_jump, test
from app.lib import set_factorycode, set_devicecode, set_totalcount, set_running_state
from app.lib import get_errno
from app.lib import testdatas_archive


blue_test = Blueprint('blue_test', __name__, url_prefix='/test')

@blue_test.route('/event1')
def event1():
    print('event1')
    ret = socketio.emit('event1', namespace='/ns1')
    return 'socketio emit event1 ' + str(ret)

 

@blue_test.route('/error')
def vf_error():
    errno = request.args.get('errno')
    return render_template('test_error.html', errno=errno)

@blue_test.route('/config')
def vf_config():
    return render_template('test_config.html')

@blue_test.route('/start')
def vf_start():
    return render_template('test_start.html')

@blue_test.route('/running')
def vf_running():
    watch_to_jump()
    return render_template('test_running.html')

@blue_test.route('/finished')
def vf_finished():
    results = TestdataView.query.all()
    control_index = request.args.get('control_index')
    # pagination code
    # PER_PAGE = 30
    # page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    # start = (page-1)*PER_PAGE
    # end = page * PER_PAGE if len(results) > page * PER_PAGE else len(results)
    # pagination = Pagination(page=page, total=len(results), per_page=PER_PAGE, bs_version=3)
    # ret = TestdataView.query.slice(start, end)
    # return render_template('testing.html', pagination=pagination, results=ret)
    return render_template('test_finished.html', results=results, control_index=control_index)


# button & command

@blue_test.route('/cmd_start_legacy', methods=['POST'])
def vf_cmd_start_legacy():
    time.sleep(1)
    # errno saved at sqlite, instead of return value here.
    # errno = start()
    start()
    # wait a second for start initializing sqlite running states
    time.sleep(1)
    return redirect(url_for('blue_test.vf_running')) 


@blue_test.route('/cmd_start', methods=['POST'])
def vf_cmd_start():
    # set_running_state()
    # watch_to_jump()
    # test()
    start()
    time.sleep(1)
    return redirect(url_for('blue_test.vf_running')) 

@blue_test.route('/cmd_saveconfig', methods=['POST'])
def vf_cmd_saveconfig():
    # devicecode = request.form.get('devicecode')
    # factorycode = request.form.get('factorycode')
    totalcount = request.form.get('totalcount')
    # set_factorycode(factorycode)
    # set_devicecode(devicecode) 
    set_totalcount(totalcount) 
    return redirect(url_for('blue_test.vf_start'))

@blue_test.route('/cmd_blink_single', methods=['POST'])
def vf_cmd_blink_single():
    mac = request.form.get('mac')
    index = request.form.get('index')
    blink_single(mac)
    return redirect(url_for('blue_test.vf_finished', control_index=index))

@blue_test.route('/cmd_blink_all', methods=['POST'])
def vf_cmd_blink_all():
    blink_all()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_blink_stop', methods=['POST'])
def vf_cmd_blink_stop():
    blink_stop()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/process_finished')
def process_finished():
    errno = get_errno()
    if errno == 0:
        testdatas_archive()
        return redirect(url_for('blue_test.vf_finished'))
    else:
        return redirect(url_for('blue_test.vf_error', errno=errno))



