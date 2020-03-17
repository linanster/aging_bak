from flask import Blueprint, request, render_template, flash, redirect, url_for
from pipe_nonblock import Pipe

from app.lib import start, stop, turn_on_off, cleanup_temp, cleanup_stage, migrate_to_archive


blue_command = Blueprint('blue_command', __name__)


@blue_command.route('/cmd_start/', methods=['POST'])
def cmd_start():
    devicecode = request.form.get('devicecode')
    factoryid = request.form.get('factoryid')
    cleanup_temp()
    errno = start(devicecode, factoryid)
    # flash('Started!')
    return redirect(url_for('blue_nav.testing'))

@blue_command.route('/cmd_stop/', methods=['POST'])
def cmd_stop():
    print("[debug] press stop")
    errno = stop()
    if 0 == errno:
        # flash('Stopped!')
        pass
    else:
        # flash('stop error')
        pass
    return redirect(url_for('blue_database.info_aging'))

@blue_command.route('/cmd_on_off/', methods=['POST'])
def cmd_on_off():
    index = request.form.get('index')
    mac = request.form.get('mac')
    on_off = request.form.get('on_off')
    print("[debug] press turn {} #{} with Mac {}".format(on_off, index, mac))
    errno = turn_on_off(mac, on_off)
    flash('Turn {} #{} with mac {}'.format(on_off, index, mac))
    return redirect(url_for('blue_database.info_aging'))

