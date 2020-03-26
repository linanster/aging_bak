from app.models import db,RunningState,Systeminfo

def get_running_state():
    r = RunningState.query.filter_by(key='s_running').first()
    return r.value1

def set_running_state():
    r = RunningState.query.filter_by(key='s_running').first()
    r.value1 = True
    db.session.commit()

def reset_running_state():
    r = RunningState.query.filter_by(key='s_running').first()
    r.value1 = False
    db.session.commit()

def set_factorycode(code):
    s = Systeminfo.query.filter_by(key='s_factorycode').first()
    s.value2 = code
    db.session.commit()


def get_factorycode():
    s = Systeminfo.query.filter_by(key='s_factorycode').first()
    return r.value2


def set_devicecode(code):
    r = RunningState.query.filter_by(key='s_devicecode').first()
    r.value2 = code
    db.session.commit()


def get_devicecode():
    r = RunningState.query.filter_by(key='s_devicecode').first()
    return r.value2

