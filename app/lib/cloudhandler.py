import copy
import json
import time
import datetime
import requests

from app.models import db, Testdata, TestdataArchive

from app.myglobal import RETENTION

from .mylogger import logger_cloud

def _check_cloud_connection():
    method = 'GET'
    ############################################
    url = "http://10.30.30.101:8000/ping"
    ############################################
    headers = {}
    payload = {}
    try:
        response = requests.request(method=method, url=url, headers=headers, data=payload, timeout=20)
        # msg = response.content
        # msg = response.text
    except Exception as e:
        logger_cloud.error(str(e))
        return False
    else:
        if response.ok and response.text == 'pong':
            return True
        else:
            return False
    

def upload_to_cloud():
    logger_cloud.warn('upload_to_cloud: start')
    # 0. check network status
    if not _check_cloud_connection():
        logger_cloud.error('upload_to_cloud: connection error')
        return 1

    try:
        # 1. fetch data from database
        datas_raw = TestdataArchive.query.all()
        datas_rdy = list()
        for item in datas_raw:
            entry = copy.deepcopy(item.__dict__)
            entry.pop('_sa_instance_state')
            entry.pop('id')
            datetime_obj = entry.get('datetime')
            datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
            datetime_dict = {'datetime': datetime_str}
            is_sync_dict = {'is_sync': True}
            entry.update(datetime_dict)
            entry.update(is_sync_dict)
            datas_rdy.append(entry)
    
        # 2. assemble api request message
        request_msg = dict()
        pin = str(time.time())
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
        dict_pin = {'pin': pin}
        dict_timestamp = {'timestamp': timestamp}
        dict_data = {'testdatas': datas_rdy}
        request_msg.update(dict_pin)
        request_msg.update(dict_timestamp)
        request_msg.update(dict_data)
    
        # 3. send message via http post method
        method = 'POST'
        ############################################
        url = "http://10.30.30.101:8000/upload"
        ############################################
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        payload = json.dumps(request_msg)
        
        # 4. send request
        response = requests.request(method=method, url=url, headers=headers, data=payload)
        
        # 5. take response
        response_msg = response.json()
   
    except Exception as e:
        logger_cloud.error('upload_to_cloud: exception when uploading data to cloud')
        logger_cloud.error(str(e))
        return 5
    

    # 6. error handler
    if response_msg.get('errno') == 1:
        logger_cloud.error('upload_to_cloud: response errno error')
        return 2
    if response_msg.get('pin') != pin:
        logger_cloud.error('cloud_to_cloud: pin mismatch error')
        return 3

    # 7. save data entries into database
    try:
        for item in datas_raw:
            item.is_sync = True
            db.session.add(item)
    except Exception as e:
        db.session.rollback()
        logger_cloud.error('upload_to_cloud: exception when updating database field is_sync')
        logger_cloud.error(str(e))
        return 4
    else:
        db.session.commit()
        logger_cloud.info('upload_to_cloud: success')
        return 0


def purge_local_archive():
    logger_cloud.info('purge_local_archive: start')
    items = TestdataArchive.query.all()
    d_now = datetime.datetime.now()
    try:
        for item in items:
            d_item = item.datetime
            # (a)production requirement
            day_range = (d_now - d_item).days
            # (b)test convenience
            # day_range = (d_now - d_item).seconds
            if day_range >= RETENTION:
                db.session.delete(item)
    except Exception as e:
        db.session.rollback()
        logger_cloud.error('purge_local_archive: exception')
        logger_cloud.error(str(e))
        return 1
    else:
        db.session.commit()
        logger_cloud.info('purge_local_archive: success')
        return 0
    
