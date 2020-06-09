# coding:utf8
#
from threading import Lock
from flask import Flask, render_template, session, request, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
import subprocess
import os

from myglobals import logfolder

async_mode = None

app_aging_logmonitor = Flask(__name__, template_folder='.')
app_aging_logmonitor.config['SECRET_KEY'] = 'secret!'
app_aging_logmonitor.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app_aging_logmonitor, async_mode=async_mode)
thread = None
thread_lock = Lock()

def watch_log():
    logfile = os.path.join(logfolder, 'log_app.txt')
    # logfile = '/root/aging/logs/log_app.txt'
    p = subprocess.Popen("tail -f {}".format(logfile), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = p.stdout.readline().decode('utf-8')[0:-1]
        socketio.emit('mylog', output, namespace='/test', broadcast=True)

@app_aging_logmonitor.route('/')
@app_aging_logmonitor.route('/index')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(watch_log)
    emit('test', {'data': 'Connected', 'count': 0})

