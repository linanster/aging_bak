#! /usr/bin/env python3
# coding:utf8
#
from flask import Flask, request, render_template, flash, redirect, url_for
import json, time
# from multiprocessing import Process, Pipe
from pipe_nonblock import Pipe
from lib import mydb
from lib import mycmd

app = Flask(__name__)

app.config['SECRET_KEY'] = "random string"

pipe1_start, pipe1_stop = Pipe(duplex=True, conn1_nonblock=False, conn2_nonblock=False)
pipe2_start, pipe2_stop = Pipe(duplex=True, conn1_nonblock=True, conn2_nonblock=True)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def handle_index():
    return render_template('index.html')

@app.route('/info_aging/', methods=['GET'])
def handle_info_aging():
    results = mydb.query_aging_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_aging.html', results=results)
@app.route('/info_device/', methods=['GET'])
def handle_info_device():
    results = mydb.query_device_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_device.html', results=results)
@app.route('/info_factory/', methods=['GET'])
def handle_info_factory():
    results = mydb.query_factory_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_factory.html', results=results)

@app.route('/cmd_start/', methods=['POST'])
def handle_cmd_start():
    errno = mycmd.view_start(pipe1_start, pipe2_start)
    if 0 == errno:
        flash('Started!')
    else:
        flash('start error')
    return redirect(url_for('handle_info_aging'))


@app.route('/cmd_stop/', methods=['POST'])
def handle_cmd_stop():
    errno = mycmd.view_stop(pipe1_stop,pipe2_stop)
    if 0 == errno:
        flash('Stopped!')
    else:
        flash('stop error')
    return redirect(url_for('handle_index'))
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True, threaded=True)
