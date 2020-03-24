from flask import Blueprint, request, render_template, flash, redirect, url_for
from multiprocessing import Process
# import datetime
import pymysql

from app.models import db, tb_device_type, tb_factory, tb_data_aging
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


def cleanup_temp():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_truncate_tb_data_aging)
    cursor.close()
    conn.commit()
    conn.close()

