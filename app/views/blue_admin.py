from flask import Blueprint, request, render_template, flash, redirect, url_for
import os
import stat

from app.lib import viewfunclog

from app.settings import gofolder

blue_admin = Blueprint('blue_admin', __name__, url_prefix='/admin')

@blue_admin.route('/configfile')
@viewfunclog
def vf_configfile():
    return render_template('admin_configfile.html')


@blue_admin.route('/upload', methods=['POST'])
@viewfunclog
def cmd_upload_configfile():
    file = request.files['file']
    if file.filename == '':
        flash('请选择文件!')
    if file:
        # filename = secure_filename(file.filename)            
        filename = 'config.json'
        destfile = os.path.join(gofolder, filename)
        file.save(destfile)
        os.chmod(destfile, stat.S_IROTH)
        flash('配置文件导入成功!')
    return redirect(url_for('blue_admin.vf_configfile'))
