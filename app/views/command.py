from flask import Blueprint, request, render_template, flash, redirect, url_for
from pipe_nonblock import Pipe

from app.lib import start, stop, turn_on_off, cleanup_temp, cleanup_stage, migrate_to_archive


blue_command = Blueprint('blue_command', __name__)


# pipe1_recv for stop()
pipe1_recv, pipe1_send = Pipe(duplex=False, conn1_nonblock=False, conn2_nonblock=False)
pipe2_recv, pipe2_send = Pipe(duplex=False, conn1_nonblock=True, conn2_nonblock=True)


@blue_command.route('/cmd_start/', methods=['POST'])
def cmd_start():
    # errno is None
    cleanup_temp()
    errno = start(pipe2_recv, pipe1_send)
    flash('Started!')
    return redirect(url_for('blue_database.info_aging', refresh=True, started=True))

@blue_command.route('/cmd_stop/', methods=['POST'])
def cmd_stop():
    print("[debug] press stop")
    errno = stop(pipe1_recv,pipe2_send)
    if 0 == errno:
        flash('Stopped!')
    else:
        flash('stop error')
    return redirect(url_for('blue_database.info_aging'))

@blue_command.route('/cmd_on_off/', methods=['POST'])
def cmd_on_off():
    mac = request.form.get('mac')
    on_off = request.form.get('on_off')
    print("[debug] press turn {} {}".format(on_off, mac))
    errno = turn_on_off(mac, on_off)
    flash('Turn {} {}'.format(on_off, mac))
    return redirect(url_for('blue_database.info_aging'))
