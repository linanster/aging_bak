#! /usr/bin/env python
# coding:utf8
#
from flask import Flask, request, render_template
import MySQLdb
import json
from lib import mydb
from lib import mycmd



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def handle_index():
    return render_template('index.html')

@app.route('/info_aging', methods=['GET'])
def handle_info_aging():
    results = mydb.query_aging_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_aging.html', results=results)
@app.route('/info_device', methods=['GET'])
def handle_info_device():
    results = mydb.query_device_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_device.html', results=results)
@app.route('/info_factory', methods=['GET'])
def handle_info_factory():
    results = mydb.query_factory_all()
    if results == 1:
        return "查询数据库失败: " + str(1)
    return render_template('db_query_factory.html', results=results)

@app.route('/cmd_start', methods=['POST'])
def handle_cmd_start():
    errno = mycmd.start()
    if errno == 0:
        return json.loads('{"cmd":"start","result":"success"}')
    else:
        return json.loads('{"cmd":"start","result":"failed","errno":%d}' % errno)

@app.route('/cmd_stop', methods=['POST'])
def handle_cmd_stop():
    errno = mycmd.stop()
    if errno == 0:
        return json.loads('{"cmd":"stop","result":"success"}')
    else:
        return json.loads('{"cmd":"stop","result":"failed","errno":%d}' % errno)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
