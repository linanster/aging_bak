from flask_sqlalchemy import SQLAlchemy
import pymysql
import datetime

view = SQLAlchemy(use_native_unicode='utf8')

def init_views(app):
    view.init_app(app)

class view_data_aging(view.Model):
    id = view.Column(view.Integer, nullable=False, autoincrement=True, primary_key = True)
    device_type = view.Column(view.String(100))
    factory = view.Column(view.String(100))
    fw_version = view.Column(view.String(100))
    rssi_ble = view.Column(view.Integer)
    rssi_wifi = view.Column(view.Integer)
    mac_ble = view.Column(view.String(100))
    mac_wifi = view.Column(view.String(100))
    is_qualified = view.Column(view.Boolean)
    is_sync = view.Column(view.Boolean)
    datetime = view.Column(view.DateTime, default=datetime.datetime.now())



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

# todo: create_view is hard coded, only works for mysql (sqlite is not supported)
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


