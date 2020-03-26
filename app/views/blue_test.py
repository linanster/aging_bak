from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_parameter

from app.models import TestdataView, Testdata
from app.lib import start, turn_on_off, cleanup_temp
from app.lib import set_factorycode, set_devicecode

blue_test = Blueprint('blue_test', __name__, url_prefix='/test')



@blue_test.route('/config')
def vf_config():
    return render_template('test_config.html')

@blue_test.route('/running')
def vf_running():
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
    return render_template('test_test.html', results=results, control_index=control_index)


@blue_test.route('/finished')
def vf_finished():
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

    return render_template('xxx.html', pagination=pagination, results=ret, control_index=control_index)



# button & command

@blue_test.route('/cmd_start', methods=['GET'])
def vf_cmd_start():
    # devicecode = request.form.get('devicecode')
    # factorycode = request.form.get('factorycode')
    cleanup_temp()
    start()
    return redirect(url_for('blue_test.vf_running'))


@blue_test.route('/cmd_saveconfig', methods=['POST'])
def vf_cmd_saveconfig():
    devicecode = request.form.get('devicecode')
    factorycode = request.form.get('factorycode')
    if not check_input_save():
         flash('保存失败')
         return redirect(url_for('blue_test.vf_config'))
    set_factorycode(factorycode)
    set_devicecode(devicecode) 
    flash('保存成功')
    return redirect(url_for('blue_test.vf_config'))

@blue_test.route('/cmd_on_off', methods=['POST'])
def vf_cmd_on_off():
    is_testing = request.form.get('is_testing')
    index = request.form.get('index')
    mac = request.form.get('mac')
    on_off = request.form.get('on_off')
    print("[debug] press turn {} #{} with Mac {}".format(on_off, index, mac))
    errno = turn_on_off(mac, on_off)
    if is_testing:
        endpoint = 'blue_test.vf_config'
    else:
        endpoint = 'blue_manage.vf_data'
        flash('Turn {} #{} with mac {}'.format(on_off, index, mac))
    return redirect(url_for(endpoint, control_index=index))


def check_input_save():
     return True
