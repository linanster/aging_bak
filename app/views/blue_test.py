from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_parameter

from app.models import view_data_aging, tb_data_aging
from app.lib import start, stop, pause, resume, turn_on_off, cleanup_temp

blue_test = Blueprint('blue_test', __name__, url_prefix='/test')



@blue_test.route('/start')
def vf_start():
    return render_template('index.html')

@blue_test.route('/running')
def vf_running():
    # results = tb_data_aging.query.all()
    results = view_data_aging.query.all()
    control_index = request.args.get('control_index')
    # pagination code
    # PER_PAGE = 30
    # page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    # start = (page-1)*PER_PAGE
    # end = page * PER_PAGE if len(results) > page * PER_PAGE else len(results)
    # pagination = Pagination(page=page, total=len(results), per_page=PER_PAGE, bs_version=3)
    # ret = view_data_aging.query.slice(start, end)
    # return render_template('testing.html', pagination=pagination, results=ret)
    return render_template('testing.html', results=results, control_index=control_index)


@blue_test.route('/finished')
def vf_finished():
    # results = tb_data_aging.query.all()
    results = view_data_aging.query.all()
    control_index = request.args.get('control_index')

    # pagination code
    PER_PAGE = 30
    page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    start = (page-1)*PER_PAGE
    end = page * PER_PAGE if len(results) > page * PER_PAGE else len(results)
    pagination = Pagination(page=page, total=len(results), per_page=PER_PAGE, bs_version=3)
    ret = view_data_aging.query.slice(start, end)

    return render_template('xxx.html', pagination=pagination, results=ret, control_index=control_index)



# button & command
@blue_test.route('/cmd_start', methods=['POST'])
def vf_cmd_start():
    devicecode = request.form.get('devicecode')
    factoryid = request.form.get('factoryid')
    cleanup_temp()
    errno = start(devicecode, factoryid)
    # flash('Started!')
    return redirect(url_for('blue_test.vf_running'))

@blue_test.route('/cmd_stop', methods=['GET'])
def vf_cmd_stop():
    print("[debug] press stop")
    errno = stop()
    if 0 == errno:
        # flash('Stopped!')
        pass
    else:
        # flash('stop error')
        pass
    return redirect(url_for('blue_manage.vf_data'))


@blue_test.route('/cmd_on_off', methods=['POST'])
def vf_cmd_on_off():
    is_testing = request.form.get('is_testing')
    index = request.form.get('index')
    mac = request.form.get('mac')
    on_off = request.form.get('on_off')
    print("[debug] press turn {} #{} with Mac {}".format(on_off, index, mac))
    errno = turn_on_off(mac, on_off)
    if is_testing:
        endpoint = 'blue_test.vf_running'
    else:
        endpoint = 'blue_manage.vf_data'
        flash('Turn {} #{} with mac {}'.format(on_off, index, mac))
    return redirect(url_for(endpoint, control_index=index))

@blue_test.route('/cmd_pause', methods=['GET'])
def vf_cmd_pause():
    pause()
    return redirect(url_for('blue_test.vf_running'))

@blue_test.route('/cmd_resume', methods=['GET'])
def vf_cmd_resume():
    resume()
    return redirect(url_for('blue_test.vf_running'))
