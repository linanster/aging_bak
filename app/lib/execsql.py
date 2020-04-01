import pymysql

# db_addr = 'localhost'
# db_port = 3306
# db_user = 'root'
# db_passwd = '123456'
# db_name = 'ge'

from app.secret import db_addr
from app.secret import db_port
from app.secret import db_user
from app.secret import db_passwd
from app.secret import db_name

sql_create_testdatasview = '''
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

sql_delete_testdatasview = '''
    DROP VIEW testdatasview;
'''
sql_create_testdatasarchiveview = '''
    CREATE VIEW testdatasarchiveview AS 
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
        FROM testdatasarchive AS a, devices AS d, factories AS f 
        WHERE a.device_type=d.code AND a.factory=f.code;
'''

sql_delete_testdatasarchiveview = '''
    DROP VIEW testdatasarchiveview;
'''

sql_truncate_testdatas = '''
    TRUNCATE table testdatas;
'''

sql_truncate_testdatasarchive = '''
    TRUNCATE table testdatasarchive;
'''

def testdatasview_create():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_create_testdatasview)
    cursor.close()
    conn.close()

def testdatasview_delete():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_delete_testdatasview)
    cursor.close()
    conn.close()    

def testdatasarchiveview_create():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_create_testdatasarchiveview)
    cursor.close()
    conn.close()

def testdatasarchiveview_delete():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_delete_testdatasarchiveview)
    cursor.close()
    conn.close()    

def testdatas_cleanup():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_truncate_testdatas)
    cursor.close()
    conn.commit()
    conn.close()

def testdatasarchive_cleanup():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_truncate_testdatasarchive)
    cursor.close()
    conn.commit()
    conn.close()

