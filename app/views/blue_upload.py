from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory, Response

from app.models import Device, Factory, TestdataStage, TestdataArchive
from app.lib import viewfunclog, logger_app

from app.lib.cloudhandler import upload_to_cloud


blue_upload = Blueprint('blue_upload', __name__, url_prefix='/upload')


@blue_upload.route('/stage', methods=['GET'])
@viewfunclog
def vf_upload():
    count_upload_todo = len(TestdataStage.query.all())
    # count_upload_done = request.args.get('count_upload_done')
    return render_template('upload_index.html', count_upload_todo=count_upload_todo)

@blue_upload.route('/cmd_upload_stage', methods=['POST'])
@viewfunclog
def cmd_upload_stage():
    count = upload_to_cloud()
    if count < 0:
        logger_app.error('[upload] error({}), please refer to logger_cloud'.format(count))
        flash('上传失败(errno: {})'.format(count))
    else:
        logger_app.info('[upload] success(count: {})'.format(count))
        flash('上传成功，共 {} 条记录同步至云端'.format(count))
    return redirect(url_for('blue_upload.vf_upload'))

