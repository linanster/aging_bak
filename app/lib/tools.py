from app.models import db_sqlite, RunningState, Systeminfo
from app.models import db_mysql, Factory, Device

def get_gecloud_online():
    r = RunningState.query.filter_by(key='r_gecloud_online').first()
    return r.value1

def set_gecloud_online():
    r = RunningState.query.filter_by(key='r_gecloud_online').first()
    r.value1 = True
    db_sqlite.session.commit()

def reset_gecloud_online():
    r = RunningState.query.filter_by(key='r_gecloud_online').first()
    r.value1 = False
    db_sqlite.session.commit()

def get_running_state():
    r = RunningState.query.filter_by(key='r_running').first()
    return r.value1

def set_running_state():
    r = RunningState.query.filter_by(key='r_running').first()
    r.value1 = True
    db_sqlite.session.commit()

def reset_running_state():
    r = RunningState.query.filter_by(key='r_running').first()
    r.value1 = False
    db_sqlite.session.commit()

def set_factorycode(code):
    s = Systeminfo.query.filter_by(key='s_factorycode').first()
    s.value2 = code
    db_sqlite.session.commit()


def get_factorycode():
    s = Systeminfo.query.filter_by(key='s_factorycode').first()
    return s.value2


def set_devicecode(num):
    r = RunningState.query.filter_by(key='r_devicecode').first()
    r.value2 = num
    db_sqlite.session.commit()


def get_devicecode():
    r = RunningState.query.filter_by(key='r_devicecode').first()
    return r.value2

def get_devicename():
    code = get_devicecode()
    # code:
    # - 0: 初始化值
    # - None: 在test_config中未设置
    if code == 0 or code is None:
        name = None
    else:
        name = Device.query.filter_by(code=code).first().name
    return name


def set_totalcount(num):
    r = RunningState.query.filter_by(key='r_totalcount').first()
    r.value2 = num
    db_sqlite.session.commit()


def get_totalcount():
    r = RunningState.query.filter_by(key='r_totalcount').first()
    return r.value2

def set_progress(num):
    r = RunningState.query.filter_by(key='r_progress').first()
    r.value2 = num
    db_sqlite.session.commit()


def get_progress():
    r = RunningState.query.filter_by(key='r_progress').first()
    return r.value2

def add_progress():
    r = RunningState.query.filter_by(key='r_progress').first()
    r.value2 += 25
    db_sqlite.session.commit()
    
def reset_progress():
    r = RunningState.query.filter_by(key='r_progress').first()
    r.value2 = 0
    db_sqlite.session.commit()



def get_phase():
    r = RunningState.query.filter_by(key='r_phase').first()
    return r.value3

def set_phase(step):
    r = RunningState.query.filter_by(key='r_phase').first()
    r.value3 = step
    db_sqlite.session.commit()

def reset_phase():
    r = RunningState.query.filter_by(key='r_phase').first()
    r.value3 = ''
    db_sqlite.session.commit()


def get_errno():
    r = RunningState.query.filter_by(key='r_errno').first()
    return r.value2
def set_errno(num):
    r = RunningState.query.filter_by(key='r_errno').first()
    r.value2 = num
    db_sqlite.session.commit() 
def reset_errno():
    r = RunningState.query.filter_by(key='r_errno').first()
    r.value2 = 0
    db_sqlite.session.commit() 


def set_fwversion(version):
    r = RunningState.query.filter_by(key='r_fwversion').first()
    r.value3 = version
    db_sqlite.session.commit()
def get_fwversion():
    r = RunningState.query.filter_by(key='r_fwversion').first()
    return r.value3

def set_mcuversion(version):
    r = RunningState.query.filter_by(key='r_mcuversion').first()
    r.value3 = version
    db_sqlite.session.commit()
def get_mcuversion():
    r = RunningState.query.filter_by(key='r_mcuversion').first()
    return r.value3

def get_ble_strength_low():
    r = RunningState.query.filter_by(key='r_ble_strength_low').first()
    return r.value2
def set_ble_strength_low(num):
    r = RunningState.query.filter_by(key='r_ble_strength_low').first()
    r.value2 = num
    db_sqlite.session.commit() 
def get_wifi_strength_low():
    r = RunningState.query.filter_by(key='r_wifi_strength_low').first()
    return r.value2
def set_wifi_strength_low(num):
    r = RunningState.query.filter_by(key='r_wifi_strength_low').first()
    r.value2 = num
    db_sqlite.session.commit() 

def set_sqlite_value3(key, value):
    r = RunningState.query.filter_by(key=key).first()
    r.value3 = value
    db_sqlite.session.commit()
def get_sqlite_value3(key):
    r = RunningState.query.filter_by(key=key).first()
    return r.value3
