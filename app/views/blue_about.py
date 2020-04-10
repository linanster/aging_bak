from flask import Blueprint, request, render_template, flash, redirect, url_for

from app.lib import viewfunclog

blue_about = Blueprint('blue_about', __name__, url_prefix='/about')

@blue_about.route('/version')
@viewfunclog
def about():
    return render_template('about.html')
