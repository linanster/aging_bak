from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory, Response

from app.models import Device, Factory, TestdataStage, TestdataArchive
from app.lib import viewfunclog, logger_app

from app.lib.cloudhandler import upload_to_cloud, refresh_gecloud_online


blue_upload = Blueprint('blue_upload', __name__, url_prefix='/upload')


@blue_upload.route('/stage', methods=['GET'])
@viewfunclog
def vf_upload():
    refresh_gecloud_online()
    count_upload_todo = len(TestdataStage.query.all())
    # count_upload_done = request.args.get('count_upload_done')
    return render_template('upload_index.html', count_upload_todo=count_upload_todo)

@blue_upload.route('/cmd_upload_stage', methods=['POST'])
@viewfunclog
def cmd_upload_stage():
    count = upload_to_cloud()
    errtable = {
        0: '成功',
        -1: '网络连接错误',
        -2: '本地数据准备错误',
        -3: '本地发送请求异常',
        -4: '云端返回错误消息码',
        -5: '云端返回校验码不匹配',
        -6: '云端返回收到数据数目与本地发送数目不相等',
        -7: '更新本地stage数据库bool_uploaded错误',
        -8: 'stage到archive数据库迁移错误',
        -9: '清除stage数据库错误',
    }

    if count < 0:
        errno = count
        errmsg = errtable.get(errno)
        logger_app.error('[upload] error({}), please refer to logger_cloud'.format(errno))
        flash('上传失败({}): {}'.format(errno, errmsg))
    else:
        logger_app.info('[upload] success(count: {})'.format(count))
        flash('上传成功，共 {} 条记录同步至云端'.format(count))
    return redirect(url_for('blue_upload.vf_upload'))

