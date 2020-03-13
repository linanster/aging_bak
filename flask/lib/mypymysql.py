from flask import Blueprint, request, render_template, flash, redirect, url_for
from multiprocessing import Process
# import datetime
import pymysql

from models import db, db_stage, db_archive, tb_device_type, tb_factory, tb_data_aging, tb_data_aging_stage, tb_data_aging_archive
# from models import view, view_data_aging

def async_call(fn):
    def wrapper(*args, **kwargs):
        Process(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

db_addr = 'localhost'
db_port = 3306
db_user = 'root'
db_passwd = '123456'
db_name = 'ge'

sql_create_view = '''
    CREATE VIEW view_data_aging AS 
        SELECT a.id AS "id", 
            d.type AS "device_type", 
            f.name AS 'factory', 
            a.fw_version,
            a.rssi_ble,
            a.rssi_wifi,
            a.mac_ble,
            a.mac_wifi,
            a.is_qualified,
            a.is_sync,
            a.datetime 
        FROM tb_data_aging AS a, tb_device_type AS d, tb_factory AS f 
        WHERE a.device_type=d.code AND a.factory=f.id;
'''

sql_delete_view = '''
    DROP VIEW view_data_aging;
'''

sql_truncate_tb_data_aging = '''
    TRUNCATE table tb_data_aging;
'''
sql_delete_tb_data_aging = '''
    DELETE FROM tb_data_aging;
'''

sql_truncate_tb_data_aging_stage = '''
    TRUNCATE table tb_data_aging_stage;
'''

sql_truncate_tb_data_aging_archive = '''
    TRUNCATE table tb_data_aging_archive;
'''

def create_view():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_create_view)
    cursor.close()
    conn.close()

def delete_view():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_delete_view)
    cursor.close()
    conn.close()    

@async_call
def migrate_to_stage():
    records_session1 = tb_data_aging.query.all()
    # print('==records_session1==',records_session1)
    records_session2 = []
    for record_session1 in records_session1:
        record_session2 = tb_data_aging_stage(record_session1)
        records_session2.append(record_session2)
    # print('==records_session2==',records_session2)
    db_stage.session.add_all(records_session2)
    db_stage.session.commit()
    # cleanup_temp()


def migrate_to_archive():
    records_session1 = tb_data_aging_stage.query.all()
    print('==records_session1==',records_session1)
    records_session2 = []
    for record_session1 in records_session1:
        record_session2 = tb_data_aging_archive(record_session1)
        records_session2.append(record_session2)
    print('==records_session2==',records_session2)
    db_archive.session.add_all(records_session2)
    db_archive.session.commit()

def cleanup_temp():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_truncate_tb_data_aging)
    cursor.close()
    conn.commit()
    conn.close()

def cleanup_stage():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_delete_tb_data_aging_stage)
    cursor.close()
    conn.commit()
    conn.close()
