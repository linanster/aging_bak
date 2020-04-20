from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory
import os
import stat
from werkzeug.utils import secure_filename

from app.lib import viewfunclog

from app.settings import gofolder

blue_admin = Blueprint('blue_admin', __name__, url_prefix='/admin')

@blue_admin.route('/go')
@viewfunclog
def vf_go():
    invisible = ['.keep', '.gitkeep', 'ble-backend-nan', 'ble-backend.bak', 'config.json.bak']
    filelist = os.listdir(gofolder)
    for filename in invisible:
        if filename in filelist:
            filelist.remove(filename)
        else:
            continue
    return render_template('admin_go.html', filelist=filelist)


@blue_admin.route('/upload', methods=['POST'])
@viewfunclog
def cmd_upload_file():
    file = request.files['file']
    if file.filename == '':
        flash('请选择文件!')
    if file:
        filename = secure_filename(file.filename)            
        # filename = 'config.json'
        destfile = os.path.join(gofolder, filename)
        file.save(destfile)
        os.chmod(destfile, stat.S_IROTH)
        flash('文件导入成功!')
    return redirect(url_for('blue_admin.vf_go'))


@blue_admin.route('/download', methods=['GET'])
@viewfunclog
def cmd_download_file():
    filename = request.args.get('filename')
    return send_from_directory(gofolder, filename, as_attachment=True)


@blue_admin.route('/view', methods=['GET'])
@viewfunclog
def cmd_view_file():
    filename = request.args.get('filename')
    return send_from_directory(gofolder, filename, as_attachment=False)

@blue_admin.route('/delete', methods=['GET'])
@viewfunclog
def cmd_delete_file():
    filename = request.args.get('filename')
    sourcefile = os.path.join(gofolder, filename)
    os.remove(sourcefile)
    return redirect(url_for('blue_admin.vf_go'))
