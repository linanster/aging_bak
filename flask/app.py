#! /usr/bin/env python3
# coding:utf8
#
from flask import Flask, request, render_template, flash, redirect, url_for
import json, time
from lib import mydb
from lib import mycmd

STOP = False
STOPPED = False

app = Flask(__name__)

app.config['SECRET_KEY'] = "random string"

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
    global STOP
    global STOPPED
    # 1.start
    errno = mycmd.start()
    if errno != 0:
        return json.dumps({"cmd":"start","result":"failed","errno":errno})
    time.sleep(60) 
    # 2.change mesh
    loop = 4
    while loop > 0:
        errno = mycmd.changemesh()
        if errno != 0:
            return json.dumps({"cmd":"changemesh","result":"failed","errno":errno})
        time.sleep(10)
        loop = loop -1
    # 3.scan
    while not STOP:
        errno = mycmd.scan()
        if errno != 0:
            return json.dumps({"cmd":"scan","result":"failed","errno":errno})
        time.sleep(10)        
    STOPPED = True
    return redirect(url_for('handle_info_aging'))


@app.route('/cmd_changemesh/')
def handle_cmd_changemesh():
    errno = mycmd.changemesh()
    if errno == 0:
        # return json.loads('{"cmd":"changemesh","result":"success"}')
        return json.dumps({"cmd":"changemesh","result":"success"})
    else:
        # return json.loads('{"cmd":"changemesh","result":"failed","errno":%d}' % errno)
        return json.dumps({"cmd":"changemesh","result":"failed","errno":errno})

@app.route('/cmd_scan/')
def handle_cmd_scan():
    errno = mycmd.scan()
    if errno == 0:
        # return json.loads('{"cmd":"scan","result":"success"}')
        return json.dumps({"cmd":"scan","result":"success"})
    else:
        # return json.loads('{"cmd":"scan","result":"failed","errno":%d}' % errno)
        return json.dumps({"cmd":"scan","result":"failed","errno":errno})

@app.route('/cmd_stop/', methods=['POST'])
def handle_cmd_stop():
    global STOP
    global STOPPED
    STOP = True
    while not STOPPED:
        time.sleep(1)
    flash('Stopped success!')
    return redirect(url_for('handle_index'))
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True, threaded=True)
