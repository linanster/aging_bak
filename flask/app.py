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

# pipe1_recv for stop()
pipe1_recv, pipe1_send = Pipe(duplex=False, conn1_nonblock=False, conn2_nonblock=False)
pipe2_recv, pipe2_send = Pipe(duplex=False, conn1_nonblock=True, conn2_nonblock=True)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/info_aging/', methods=['GET'])
def info_aging():
    results = mydb.query_aging_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_aging.html', results=results)
@app.route('/info_device/', methods=['GET'])
def info_device():
    results = mydb.query_device_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_device.html', results=results)
@app.route('/info_factory/', methods=['GET'])
def info_factory():
    results = mydb.query_factory_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_factory.html', results=results)

@app.route('/cmd_start/', methods=['POST'])
def cmd_start():
    # errno is None
    errno = mycmd.start(pipe2_recv, pipe1_send)
    flash('Started!')
    return redirect(url_for('index'))


@app.route('/cmd_stop/', methods=['POST'])
def cmd_stop():
    print("[debug] press stop")
    errno = mycmd.stop(pipe1_recv,pipe2_send)
    if 0 == errno:
        flash('Stopped!')
    else:
        flash('stop error')
    return redirect(url_for('index'))
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True, threaded=True)
