import pymysql
import sqlite3
import os

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

from app.myglobals import sqlitefolder

dbfile = os.path.abspath(os.path.join(sqlitefolder, "system.sqlite3"))

sql_get_running_state = '''
    SELECT value1 FROM runningstates WHERE key='r_running';
'''

sql_get_retried = '''
    SELECT value1 FROM runningstates WHERE key='r_retried';
'''
sql_set_retried = '''
    UPDATE runningstates SET value1=1 WHERE key='r_retried';
'''
sql_reset_retried = '''
    UPDATE runningstates SET value1=0 WHERE key='r_retried';
'''

sql_truncate_testdatas = '''
    TRUNCATE table testdatas;
'''

sql_truncate_testdatasarchive = '''
    TRUNCATE table testdatasarchive;
'''

def sql_testdatas_cleanup():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_truncate_testdatas)
    cursor.close()
    conn.commit()
    conn.close()

def sql_testdatasarchive_cleanup():
    conn = pymysql.Connect(host=db_addr, port=db_port, user=db_user, passwd=db_passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql_truncate_testdatasarchive)
    cursor.close()
    conn.commit()
    conn.close()

def get_running_state_sql():
    conn = sqlite3.connect(dbfile)
    cursor = conn.execute(sql_get_running_state)
    res = cursor.fetchone()
    return res[0]

def get_retried_sql():
    conn = sqlite3.connect(dbfile)
    cursor = conn.execute(sql_get_retried)
    res = cursor.fetchone()
    return res[0]
def set_retried_sql():
    conn = sqlite3.connect(dbfile)
    cursor = conn.execute(sql_set_retried)
    conn.commit()
    conn.close()
def reset_retried_sql():
    conn = sqlite3.connect(dbfile)
    cursor = conn.execute(sql_reset_retried)
    conn.commit()
    conn.close()
