import pymysql

# db_addr = 'localhost'
# db_port = 3306
# db_user = 'root'
# db_passwd = '123456'
# db_name = 'ge'

from app.secret import db_addr, db_port, db_user, db_passwd, db_name

sql_create_view = '''
    CREATE VIEW testdatasview AS 
        SELECT a.id AS "id", 
            d.name AS "device_type", 
            f.name AS 'factory', 
            a.fw_version,
            a.rssi_ble,
            a.rssi_wifi,
            a.mac_ble,
            a.mac_wifi,
            a.is_qualified,
            a.is_sync,
            a.datetime 
        FROM testdatas AS a, devices AS d, factories AS f 
        WHERE a.device_type=d.code AND a.factory=f.code;
'''

sql_delete_view = '''
    DROP VIEW testdatasview;
'''

sql_truncate_testdatas = '''
    TRUNCATE table testdatas;
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
    cursor.execute(sql_truncate_testdatas)
    cursor.close()
    conn.commit()
    conn.close()

