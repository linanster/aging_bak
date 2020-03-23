from app.models import db
from app.models import tb_state

def get_stopped_state():
    r = tb_state.query.filter_by(metric='s_stopped').first()
    return r.state

def set_stopped_state():
    r = tb_state.query.filter_by(metric='s_stopped').first()
    r.state = True
    db.session.commit()

def reset_stopped_state():
    r = tb_state.query.filter_by(metric='s_stopped').first()
    r.state = False
    db.session.commit()

def get_stop_action():
    r = tb_state.query.filter_by(metric='a_stop').first()
    return r.state

def set_stop_action():
    r = tb_state.query.filter_by(metric='a_stop').first()
    r.state = True
    db.session.commit()

def reset_stop_action():
    r = tb_state.query.filter_by(metric='a_stop').first()
    r.state = False
    db.session.commit()

def get_paused_state():
    r = tb_state.query.filter_by(metric='s_paused').first()
    return r.state

def set_paused_state():
    r = tb_state.query.filter_by(metric='s_paused').first()
    r.state = True
    db.session.commit()

def reset_paused_state():
    r = tb_state.query.filter_by(metric='s_paused').first()
    r.state = False
    db.session.commit()


def get_pause_action():
    r = tb_state.query.filter_by(metric='a_pause').first()
    return r.state

def set_pause_action():
    r = tb_state.query.filter_by(metric='a_pause').first()
    r.state = True
    db.session.commit()

def reset_pause_action():
    r = tb_state.query.filter_by(metric='a_pause').first()
    r.state = False
    db.session.commit()