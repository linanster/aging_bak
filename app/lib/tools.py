from app.models import db,RunningState,Systeminfo

def get_running_state():
    r = RunningState.query.filter_by(key='r_running').first()
    return r.value1

def set_running_state():
    r = RunningState.query.filter_by(key='r_running').first()
    r.value1 = True
    db.session.commit()

def reset_running_state():
    r = RunningState.query.filter_by(key='r_running').first()
    r.value1 = False
    db.session.commit()

def set_factorycode(code):
    s = Systeminfo.query.filter_by(key='s_factorycode').first()
    s.value2 = code
    db.session.commit()


def get_factorycode():
    s = Systeminfo.query.filter_by(key='s_factorycode').first()
    return r.value2


def set_devicecode(num):
    r = RunningState.query.filter_by(key='r_devicecode').first()
    r.value2 = num
    db.session.commit()


def get_devicecode():
    r = RunningState.query.filter_by(key='r_devicecode').first()
    return r.value2

def set_totalcount(num):
    r = RunningState.query.filter_by(key='r_totalcount').first()
    r.value2 = num
    db.session.commit()


def get_totalcount():
    r = RunningState.query.filter_by(key='r_totalcount').first()
    return r.value2

def set_progress(num):
    r = RunningState.query.filter_by(key='r_progress').first()
    r.value2 = num
    db.session.commit()


def get_progress():
    r = RunningState.query.filter_by(key='r_progress').first()
    return r.value2

def add_progress():
    r = RunningState.query.filter_by(key='r_progress').first()
    r.value2 += 25
    db.session.commit()
    
def reset_progress():
    r = RunningState.query.filter_by(key='r_progress').first()
    r.value2 = 0
    db.session.commit()
