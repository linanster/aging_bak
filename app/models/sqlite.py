from flask_sqlalchemy import SQLAlchemy
import datetime


# 1 -- Leedarson
# 2 -- Innotech
# 3 -- Tonly
# 4 -- Changhong
# 5 -- Test
from app.fcode import FCODE

# 1. lasy init
db_sqlite = SQLAlchemy(use_native_unicode='utf8')



# 2. model definition

class RunningState(db_sqlite.Model):
    __bind_key__ = 'sqlite'
    __tablename__ = 'runningstates'
    id = db_sqlite.Column(db_sqlite.Integer, nullable=False, autoincrement=True, primary_key=True)
    key = db_sqlite.Column(db_sqlite.String(100))
    value1 = db_sqlite.Column(db_sqlite.Boolean)
    value2 = db_sqlite.Column(db_sqlite.Integer)
    value3 = db_sqlite.Column(db_sqlite.String(100))
    description = db_sqlite.Column(db_sqlite.String(100))
    def __init__(self, key, value1=False, value2=-100, value3='', description=''):
        self.key = key
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.description = description
    @staticmethod
    def seed():
        r_gecloud_online = RunningState('r_gecloud_online', value1=False, description='Indicate gecloud reachable or not, default is False.')
        r_running = RunningState('r_running', value1=False, description='Indicate running or not, default is False.')
        r_eventdone = RunningState('r_eventdone', value1=False, description='Indicate event done received by web client.')
        r_devicecode = RunningState('r_devicecode', value2=0)
        r_totalcount = RunningState('r_totalcount', value2=0) 
        r_progress = RunningState('r_progress', value2=0) 
        r_phase = RunningState('r_phase', value3='')
        r_errno = RunningState('r_errno', value2=0) 
        r_retried = RunningState('r_retried', value1=False) 
        r_fwversion = RunningState('r_fwversion', value3='noversion') 
        r_mcuversion = RunningState('r_mcuversion', value3='noversion') 
        r_ble_strength_low = RunningState('r_ble_strength_low', value2=-100) 
        r_wifi_strength_low = RunningState('r_wifi_strength_low', value2=-100) 
        r_wifi_mac_low = RunningState('r_wifi_mac_low', value3='000000000000')
        r_wifi_mac_high = RunningState('r_wifi_mac_high', value3='000000000000')
        r_ble_mac_low = RunningState('r_ble_mac_low', value3='000000000000')
        r_ble_mac_high = RunningState('r_ble_mac_high', value3='000000000000')
        r_test_mode = RunningState('r_test_mode', value3='production')
        seeds = [r_gecloud_online, r_running, r_devicecode, r_totalcount, r_progress, r_phase, r_errno, r_retried, r_fwversion, r_mcuversion, r_ble_strength_low, r_wifi_strength_low, r_eventdone,
            r_wifi_mac_low, r_wifi_mac_high, r_ble_mac_low, r_ble_mac_high,
            r_test_mode,
        ]
        db_sqlite.session.add_all(seeds)
        db_sqlite.session.commit()

class Systeminfo(db_sqlite.Model):
    __bind_key__ = 'sqlite'
    __tablename__ = 'systeminfo'
    id = db_sqlite.Column(db_sqlite.Integer, nullable=False, autoincrement=True, primary_key=True)
    key = db_sqlite.Column(db_sqlite.String(100))
    value1 = db_sqlite.Column(db_sqlite.Boolean)
    value2 = db_sqlite.Column(db_sqlite.Integer)
    description = db_sqlite.Column(db_sqlite.String(100))
    def __init__(self, key, value1=False, value2=-100, description=''):
        self.key = key
        self.value1 = value1
        self.value2 = value2
        self.description = description
    @staticmethod
    def seed():
        s_factorycode = Systeminfo('s_factorycode', value2=FCODE)
        seeds = [s_factorycode,]
        db_sqlite.session.add_all(seeds)
        db_sqlite.session.commit()

