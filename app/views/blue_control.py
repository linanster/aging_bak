from flask import Blueprint, request, render_template, flash, redirect, url_for

from app.lib import viewfunclog

blue_control = Blueprint('blue_control', __name__, url_prefix='/control')

@blue_control.route('/system')
@viewfunclog
def vf_system():
    return render_template('control_system.html')

@blue_control.route('/onlinecmd')
@viewfunclog
def vf_onlinecmd():
    return render_template('control_onlinecmd.html')
