#! /usr/bin/env python2
# coding: utf8
#
import MySQLdb

# predefined variables
db_addr = 'localhost'
db_port = 3306
db_user = 'root'
db_passwd = '123456'
db_name = 'ge'


# sql_query_aging_all = 'SELECT id,device_type,factory,fw_version,rssi_ble,rssi_wifi,mac_ble,mac_wifi,is_qualified,is_sync,datetime FROM tb_data_aging'
sql_query_aging_all = 'SELECT id,device_type,factory,fw_version,rssi_ble,rssi_wifi,mac_ble,mac_wifi,is_qualified,is_sync,datetime FROM view_data_aging'
sql_query_device_all = 'SELECT code,type,detail,description FROM tb_device_type'
sql_query_factory_all = 'SELECT id,name,description from tb_factory'

def query_aging_all():
    try:
        conn = MySQLdb.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    except Exception as e:
        print "连接数据库失败: " + str(e)
        results = 1
    else:
        cursor = conn.cursor()
        cursor.execute(sql_query_aging_all)
        # results probably is [], no data queried out from database
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    finally:
        return results

def query_device_all():
    try:
        conn = MySQLdb.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    except Exception as e:
        print "连接数据库失败: " + str(e)
        results = 1
    else:
        cursor = conn.cursor()
        cursor.execute(sql_query_device_all)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    finally:
        return results

def query_factory_all():
    try:
        conn = MySQLdb.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name, charset='utf8')
    except Exception as e:
        print "连接数据库失败: " + str(e)
        results = 1
    else:
        cursor = conn.cursor()
        cursor.execute(sql_query_factory_all)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    finally:
        return results
