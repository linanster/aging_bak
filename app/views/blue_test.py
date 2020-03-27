from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_parameter

from app.models import TestdataView, Testdata
from app.lib import start, blink_single, blink_all, blink_stop, cleanup_temp
from app.lib import set_factorycode, set_devicecode, set_totalcount

blue_test = Blueprint('blue_test', __name__, url_prefix='/test')



@blue_test.route('/config')
def vf_config():
    return render_template('test_config.html')

@blue_test.route('/start')
def vf_start():
    return render_template('test_start.html')

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

@blue_test.route('/cmd_start', methods=['POST'])
def vf_cmd_start():
    cleanup_temp()
    start()
    return redirect(url_for('blue_test.vf_finished'))


@blue_test.route('/cmd_saveconfig', methods=['POST'])
def vf_cmd_saveconfig():
    # devicecode = request.form.get('devicecode')
    # factorycode = request.form.get('factorycode')
    totalcount = request.form.get('totalcount')
    if not check_input_save():
         flash('保存失败')
         return redirect(url_for('blue_test.vf_config'))
    # set_factorycode(factorycode)
    # set_devicecode(devicecode) 
    set_totalcount(totalcount) 
    return redirect(url_for('blue_test.vf_start'))

@blue_test.route('/cmd_blink_single', methods=['POST'])
def vf_cmd_blink_single():
    mac = request.form.get('mac')
    index = request.form.get('index')
    print("==blink mac==",mac)
    blink_single(mac)
    return redirect(url_for('blue_test.vf_finished', control_index=index))

@blue_test.route('/cmd_blink_all', methods=['POST'])
def vf_cmd_blink_all():
    print("==blink all==")
    blink_all()
    return redirect(url_for('blue_test.vf_finished'))

@blue_test.route('/cmd_blink_stop', methods=['POST'])
def vf_cmd_blink_stop():
    print("==blink stop==")
    blink_stop()
    return redirect(url_for('blue_test.vf_finished'))

def check_input_save():
     return True
