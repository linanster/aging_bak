from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory
from flask_paginate import Pagination, get_page_parameter
import time
import datetime
import os

from app.models import Testdata, Factory, Device
from app.lib import start, blink_single, blink_all, blink_failed, blink_stop, turn_on_all, turn_off_all, kickout_all, indicator_r, indicator_g, indicator_b
from app.lib import watch_to_jump, watch_timeout, watch_to_blink
from app.lib import set_factorycode, set_devicecode, set_totalcount, set_running_state, set_fwversion, set_mcuversion, set_ble_strength_low, set_wifi_strength_low
from app.lib import get_errno, get_running_state, get_factorycode
from app.lib import testdatas_archive
from app.lib import viewfunclog
from app.lib import logger_app
from app.lib import gen_excel, empty_folder
from app.lib.myutils import write_json_to_file

from app.myglobals import topdir, gofolder


blue_test = Blueprint('blue_test', __name__, url_prefix='/test')


@blue_test.route('/error')
@viewfunclog
def vf_error():
    errno = request.args.get('errno')
    return render_template('test_error.html', errno=errno)

@blue_test.route('/config')
@viewfunclog
def vf_config():
    fcode = get_factorycode()
    if fcode == 0:
        devices = Device.query.all()
    elif fcode in (1, 2, 3, 4, 5):
        # factory = Factory.query.filter(Factory.code.__eq__(fcode)).first()
        factory = Factory.query.filter(Factory.code == fcode).first()
        devices = factory.devices
    else:
        devices = list()
    
    return render_template('test_config.html', devices=devices)

@blue_test.route('/tips_mcu')
@viewfunclog
def vf_tips_mcu():
    return render_template('tips_test_mcu.html')


@blue_test.route('/start')
@viewfunclog
def vf_start():
    return render_template('test_start.html')

@blue_test.route('/running')
@viewfunclog
def vf_running():
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

@blue_test.route('/logmonitor')
@viewfunclog
def vf_logmonitor():
    return render_template('test_logmonitor.html')

# button & command

@blue_test.route('/cmd_start', methods=['POST'])
@viewfunclog
def vf_cmd_start():
    time.sleep(1)
    logger_app.warn('click start button')
    set_running_state()
    start()
    watch_timeout()
    watch_to_jump()
    watch_to_blink()
    return redirect(url_for('blue_test.vf_running')) 


@blue_test.route('/cmd_saveconfig', methods=['POST'])
@viewfunclog
def vf_cmd_saveconfig():
    # factorycode = request.form.get('factorycode')
    devicecode = request.form.get('devicecode', type=int)
    totalcount = request.form.get('totalcount', type=int)
    fwversion = request.form.get('fwversion', type=str)
    mcuversion = request.form.get('mcuversion', type=str)
    ble_strength_low = request.form.get('ble_strength_low', type=int)
    wifi_strength_low = request.form.get('wifi_strength_low', type=int)
    if len(mcuversion) == 0:
        mcuversion = '0'
    if ble_strength_low is None:
        ble_strength_low = -100
    if wifi_strength_low is None:
        wifi_strength_low = -110
    set_devicecode(devicecode) 
    set_totalcount(totalcount) 
    set_fwversion(fwversion)
    set_mcuversion(mcuversion)
    set_ble_strength_low(ble_strength_low)
    set_wifi_strength_low(wifi_strength_low)

    dict_params = {
        'devicecode': devicecode,
        'totalcount': totalcount,
        'fwversion': fwversion,
        'mcuversion': mcuversion,
        'ble_strength_low': ble_strength_low,
        'wifi_strength_low': wifi_strength_low,
    }
    filename = os.path.join(gofolder, 'params.json')
    write_json_to_file(dict_params, filename)

    return redirect(url_for('blue_test.vf_start'))

@blue_test.route('/cmd_blink_single', methods=['POST'])
@viewfunclog
def vf_cmd_blink_single():
    logger_app.warn('click blink single button')
    mac = request.form.get('mac')
    index = request.form.get('index')
    blink_single(mac)
    return redirect(url_for('blue_test.vf_finished', control_index=index))

@blue_test.route('/cmd_blink_all', methods=['POST'])
@viewfunclog
def vf_cmd_blink_all():
    logger_app.warn('click blink all button')
    blink_all()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_blink_failed', methods=['POST'])
@viewfunclog
def vf_cmd_blink_failed():
    logger_app.warn('click blink failed button')
    blink_failed()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_blink_stop', methods=['POST'])
@viewfunclog
def vf_cmd_blink_stop():
    logger_app.warn('click blink stop button')
    blink_stop()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_allon', methods=['POST'])
@viewfunclog
def cmd_allon():
    logger_app.warn('click turn on all button')
    turn_on_all()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_alloff', methods=['POST'])
@viewfunclog
def cmd_alloff():
    logger_app.warn('click turn off all button')
    turn_off_all()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_kickout', methods=['POST'])
@viewfunclog
def cmd_kickout():
    logger_app.warn('click kickout button')
    kickout_all()
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
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    excelname = 'Testdata-' + timestamp + '.xls'
    excelfolder = os.path.join(topdir, 'pub', 'excel')
    filename = os.path.join(excelfolder, excelname)
    empty_folder(excelfolder)    
    gen_excel(Testdata, filename)
    return send_from_directory(excelfolder, excelname, as_attachment=True)

@blue_test.route('/cmd_indicator_r', methods=['POST'])
@viewfunclog
def cmd_indicator_r():
    logger_app.warn('click indicator_r button')
    indicator_r()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_indicator_g', methods=['POST'])
@viewfunclog
def cmd_indicator_g():
    logger_app.warn('click indicator_g button')
    indicator_g()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_indicator_b', methods=['POST'])
@viewfunclog
def cmd_indicator_b():
    logger_app.warn('click indicator_b button')
    indicator_b()
    return redirect(url_for('blue_test.vf_finished'))

