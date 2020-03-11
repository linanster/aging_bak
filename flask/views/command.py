from flask import Blueprint, request, render_template, flash, redirect, url_for
from pipe_nonblock import Pipe

from lib import mycmd

blue_command = Blueprint('blue_command', __name__)


# pipe1_recv for stop()
pipe1_recv, pipe1_send = Pipe(duplex=False, conn1_nonblock=False, conn2_nonblock=False)
pipe2_recv, pipe2_send = Pipe(duplex=False, conn1_nonblock=True, conn2_nonblock=True)


@blue_command.route('/cmd_start/', methods=['POST'])
def cmd_start():
    # errno is None
    errno = mycmd.start(pipe2_recv, pipe1_send)
    flash('Started!')
    return redirect(url_for('blue_index.index'))

@blue_command.route('/cmd_stop/', methods=['POST'])
def cmd_stop():
    print("[debug] press stop")
    errno = mycmd.stop(pipe1_recv,pipe2_send)
    if 0 == errno:
        flash('Stopped!')
    else:
        flash('stop error')
    return redirect(url_for('blue_index.index'))

