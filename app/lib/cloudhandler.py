import copy
import json
import time
import datetime
import requests

from app.models import db_mysql, Testdata, TestdataStage, TestdataArchive
from app.myglobals import RETENTION, gecloud_ip, gecloud_port, gecloud_protocol
from .mylogger import logger_cloud
from app.lib.execmodel import testdatasstage_archive, testdatasstage_cleanup_archived
from app.lib.tools import set_gecloud_online, reset_gecloud_online
from app.fcode import FCODE


def check_gecloud_connection():
    method = 'GET'
    ############################################
    url = "{}://{}:{}/api/rasp/ping".format(gecloud_protocol, gecloud_ip, gecloud_port)
    ############################################
    headers = {}
    payload = {}
    try:
        response = requests.request(method=method, url=url, headers=headers, data=payload, timeout=10, verify=False)
        # msg = response.content
        # msg = response.text
    except Exception as e:
        logger_cloud.error(str(e))
        return False
    else:
        # if response.ok and response.text == 'pong':
        if response.ok and response.json().get('msg') == 'pong':
            return True
        else:
            return False

def check_upgrade_pin(pin):
    if pin == 'youdonotknowme':
        return True
    ############################################
    url = '{}://{}:{}/api/rasp/verifypin'.format(gecloud_protocol, gecloud_ip, gecloud_port)
    ############################################
    payload = 'pin={}'.format(pin)
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data = payload, verify=False)
    return response.json().get('verified')

    

def upload_to_cloud():
    logger_cloud.info('upload_to_cloud: start')
    # 0. check network status
    if not check_gecloud_connection():
        logger_cloud.error('upload_to_cloud: connection error')
        return -1

    try:
        # 1. fetch data from database
        # datas_raw = TestdataArchive.query.all()
        # datas_raw = TestdataArchive.query.filter_by(bool_uploaded=False).all()
        # datas_raw = TestdataStage.query.all()
        datas_raw = TestdataStage.query.filter_by(bool_uploaded=False).all()
        datas_rdy = list()
        for item in datas_raw:
            entry = copy.deepcopy(item.__dict__)
            entry.pop('_sa_instance_state')
            entry.pop('id')
            datetime_obj = entry.get('datetime')
            datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
            datetime_dict = {'datetime': datetime_str}
            bool_uploaded_dict = {'bool_uploaded': True}
            entry.update(datetime_dict)
            entry.update(bool_uploaded_dict)
            datas_rdy.append(entry)
        num_raw = len(datas_raw)
        num_rdy = len(datas_rdy)
        if not num_raw == num_rdy:
            logger_cloud.error('upload_to_cloud: num_raw({}) and num_rdy({}) is not equal'.format(num_raw, num_rdy))
            return -2
        num_send = num_rdy
    
        # 2. assemble api request message
        request_msg = dict()
        pin = str(time.time())
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
        dict_fcode = {'fcode': FCODE}
        dict_pin = {'pin': pin}
        dict_timestamp = {'timestamp': timestamp}
        dict_count = {'count': num_send}
        dict_data = {'testdatas': datas_rdy}
        request_msg.update(dict_fcode)
        request_msg.update(dict_pin)
        request_msg.update(dict_timestamp)
        request_msg.update(dict_count)
        request_msg.update(dict_data)
    
        # 3. send message via http post method
        method = 'PUT'
        ############################################
        url = "{}://{}:{}/api/rasp/upload".format(gecloud_protocol, gecloud_ip, gecloud_port)
        ############################################
        headers = {
            'Authorization': 'Basic dXNlcjE6MTIzNDU2',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = json.dumps(request_msg)
        
        # 4. send request
        response = requests.request(method=method, url=url, headers=headers, data=payload, timeout=60, verify=False)
        
        # 5. take response
        response_msg = response.json()
        resp_errno = response_msg.get('errno')
        resp_msg = response_msg.get('msg')
   
    except Exception as e:
        logger_cloud.error('upload_to_cloud: exception when uploading data to cloud')
        logger_cloud.error(str(e))
        return -3
    

    # 6. error handler
    if resp_errno != 0:
        logger_cloud.error('upload_to_cloud: response error')
        logger_cloud.error(resp_msg)
        return -4
    if response_msg.get('pin') != pin:
        logger_cloud.error('upload_to_cloud: pin mismatch error')
        logger_cloud.error(resp_msg)
        return -5
    num_recv = response_msg.get('count')
    if num_recv != num_send:
        logger_cloud.error('upload_to_cloud: number send({}) and recv({}) mismatch error'.format(num_send, num_recv))
        logger_cloud.error(resp_msg)
        return -6

    num_uploaded = num_recv

    # 7. update bool_uploaded segment at local database testdatasstage
    try:
        for item in datas_raw:
            item.bool_uploaded = True
            db_mysql.session.add(item)
    except Exception as e:
        db_mysql.session.rollback()
        logger_cloud.error('upload_to_cloud: exception when updating database field bool_uploaded')
        logger_cloud.error(str(e))
        return -7
    else:
        db_mysql.session.commit()

    # 8. move data from stage to archive
    # 8.1 copy uploaded data from stage to archive
    try:
        num = testdatasstage_archive()
        logger_cloud.info('upload_to_cloud: archive success(count: {})'.format(num))
    except Exception as e:
        db_mysql.session.rollback()
        logger_cloud.error('upload_to_cloud: exception when copy uploaded data from stage to archive')
        logger_cloud.error(str(e))
        return -8
    # 8.2 clean up uploaded data at stage
    try:
        num = testdatasstage_cleanup_archived()
        logger_cloud.info('upload_to_cloud: stage cleanup success(count: {})'.format(num))
    except Exception as e:
        db_mysql.session.rollback()
        logger_cloud.error('upload_to_cloud: exception when clean up upladed data at stage')
        logger_cloud.error(str(e))
        return -9
    else:
        db_mysql.session.commit()

    # 9. write into log
    logger_cloud.info('upload_to_cloud: success(count: {})'.format(num_uploaded))
    return num_uploaded

def refresh_gecloud_online():
    if check_gecloud_connection():
        set_gecloud_online()
        return True
    else:
        reset_gecloud_online()
        return False


def purge_local_archive():
    logger_cloud.info('purge_local_archive: start')
    # items = TestdataArchive.query.all()
    items = TestdataArchive.query.filter_by(bool_uploaded=True).all()
    d_now = datetime.datetime.now()
    count = 0
    try:
        for item in items:
            d_item = item.datetime
            # retention switch between production and test
            # (a)production requirement
            day_range = (d_now - d_item).days
            # (b)test convenience
            # day_range = (d_now - d_item).seconds
            if day_range > RETENTION:
                db_mysql.session.delete(item)
                count += 1
    except Exception as e:
        db_mysql.session.rollback()
        logger_cloud.error('purge_local_archive: exception')
        logger_cloud.error(str(e))
        return 1
    else:
        db_mysql.session.commit()
        logger_cloud.info('purge_local_archive: success(count: {})'.format(count))
        return 0
    
