from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime


# 1. lasy init
db = SQLAlchemy(use_native_unicode='utf8')
db_stage = SQLAlchemy(use_native_unicode='utf8')
db_archive = SQLAlchemy(use_native_unicode='utf8')

def init_tables(app):
    db.init_app(app)
    db_stage.init_app(app)
    db_archive.init_app(app)

class tb_state(db.Model):
    __bind_key__ = 'state'
    __tablename__ = 'tb_state'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    metric = db.Column(db.String(100))
    state = db.Column(db.Boolean)
    description = db.Column(db.String(100))
    def __init__(self, metric, state=False, description=''):
        self.metric = metric
        self.state = state
        self.description = description
    def seed():
        s_running = tb_state('s_running', False, 'indicate running or not')
        s_paused = tb_state('s_paused', False, 'indicate paused or not')
        a_stop = tb_state('a_stop', False, 'indicate if stop command send out')
        db.session.add_all([s_running, a_stop, s_paused])
        db.session.commit()

# 2. model definition

class tb_device_type(db.Model):
    __bind_key__ = 'main'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    type = db.Column('type', db.String(100), nullable=False)
    detail = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tb_data_aging = db.relationship('tb_data_aging', backref='tb_device_type')
    def __init__(self, code, type, detail, description=''):
        self.code = code
        self.type = type
        self.detail = detail
        self.description = description
    @staticmethod
    def seed():
        d1 = tb_device_type(1, 'C-Life', 'Gen1/Gen2 ST C-Life(Ox01)')
        d2 = tb_device_type(17, 'C-Life', 'Gen2 Andromeda C-Life(0x11)')
        d3 = tb_device_type(18, 'C-Life', 'Gen2 MFG C-Life(0x12)')
        d4 = tb_device_type(5, 'C-Sleep', 'Gen1/Gen2 ST C-Sleep(0x05)')
        d5 = tb_device_type(19, 'C-Sleep', 'Gen2 MFG C-Sleep(0x13)')
        db.session.add_all([d1, d2, d3, d4, d5])
        db.session.commit()

class tb_factory(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'tb_factory'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    tb_data_aging = db.relationship('tb_data_aging', backref='tb_factory')
    def __init__(self, id, name, description=''):
        self.id = id
        self.name = name
        self.description = description
    @staticmethod
    def seed():
        f1 = tb_factory(1, 'Leedarson', '立达信')
        f2 = tb_factory(2, 'Innotech', 'Smart LED Light Bulbs')
        f3 = tb_factory(3, 'Tonly', '通力')
        db.session.add_all([f1, f2, f3])
        db.session.commit()

class tb_data_aging(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'tb_data_aging'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    device_type = db.Column(db.Integer, db.ForeignKey('tb_device_type.code'), nullable=False)
    factory = db.Column(db.Integer, db.ForeignKey('tb_factory.id'), nullable=False) 
    fw_version = db.Column(db.String(100))
    rssi_ble = db.Column(db.Integer)
    rssi_wifi = db.Column(db.Integer)
    mac_ble = db.Column(db.String(100))
    mac_wifi = db.Column(db.String(100))
    is_qualified = db.Column(db.Boolean)
    is_sync = db.Column(db.Boolean)
    datetime = db.Column(db.DateTime, default=datetime.datetime.now())
    def __init__(self, device_type, factory, fw_version, rssi_ble, rssi_wifi, mac_ble, mac_wifi, is_qualified, is_sync, datetime=None):
        self.device_type = device_type
        self.factory = factory
        self.fw_version = fw_version
        self.rssi_ble = rssi_ble
        self.rssi_wifi = rssi_wifi
        self.mac_ble = mac_ble
        self.mac_wifi = mac_wifi
        self.is_qualified = is_qualified
        self.is_sync = is_sync
        self.datetime = datetime
    @staticmethod
    def seed():
        a1 = tb_data_aging(5, 2, '3.1', -65, -33, 'd74d38dabcf1', '88:50:F6:04:62:31', True, False, datetime.datetime.now())
        a2 = tb_data_aging(1, 3, '3.2', -65, -33, 'd74d38dabcf5', '88:50:F6:04:62:35', True, False, datetime.datetime.now())
        a3 = tb_data_aging(17, 1, '3.40', -65, -33, 'd74d38dabcf7', '88:50:F6:04:62:37', False, False, datetime.datetime.now())
        db.session.add_all([a1, a2, a3])
        db.session.commit()

class tb_data_aging_stage(db_stage.Model):
    __bind_key__ = 'main'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    # device_type = db.Column(db.Integer, db.ForeignKey('tb_device_type.code'), nullable=False)
    # factory = db.Column(db.Integer, db.ForeignKey('tb_factory.id'), nullable=False) 
    device_type = db.Column(db.Integer, nullable=False)
    factory = db.Column(db.Integer, nullable=False) 
    fw_version = db.Column(db.String(100))
    rssi_ble = db.Column(db.Integer)
    rssi_wifi = db.Column(db.Integer)
    mac_ble = db.Column(db.String(100))
    mac_wifi = db.Column(db.String(100))
    is_qualified = db.Column(db.Boolean)
    is_sync = db.Column(db.Boolean)
    datetime = db.Column(db.DateTime)
    def __init__(self, device_type, factory, fw_version, rssi_ble, rssi_wifi, mac_ble, mac_wifi, is_qualified, is_sync, datetime):
        self.device_type = device_type
        self.factory = factory
        self.fw_version = fw_version
        self.rssi_ble = rssi_ble
        self.rssi_wifi = rssi_wifi
        self.mac_ble = mac_ble
        self.mac_wifi = mac_wifi
        self.is_qualified = is_qualified
        self.is_sync = is_sync
        self.datetime = datetime
    def __init__(self, age_obj):
        self.device_type = age_obj.device_type
        self.factory = age_obj.factory
        self.fw_version = age_obj.fw_version
        self.rssi_ble = age_obj.rssi_ble
        self.rssi_wifi = age_obj.rssi_wifi
        self.mac_ble = age_obj.mac_ble
        self.mac_wifi = age_obj.mac_wifi
        self.is_qualified = age_obj.is_qualified
        self.is_sync = age_obj.is_sync
        self.datetime = age_obj.datetime

class tb_data_aging_archive(db_archive.Model):
    __bind_key__ = 'main'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    # device_type = db.Column(db.Integer, db.ForeignKey('tb_device_type.code'), nullable=False)
    # factory = db.Column(db.Integer, db.ForeignKey('tb_factory.id'), nullable=False) 
    device_type = db.Column(db.Integer, nullable=False)
    factory = db.Column(db.Integer, nullable=False) 
    fw_version = db.Column(db.String(100))
    rssi_ble = db.Column(db.Integer)
    rssi_wifi = db.Column(db.Integer)
    mac_ble = db.Column(db.String(100))
    mac_wifi = db.Column(db.String(100))
    is_qualified = db.Column(db.Boolean)
    is_sync = db.Column(db.Boolean)
    datetime = db.Column(db.DateTime)
    def __init__(self, device_type, factory, fw_version, rssi_ble, rssi_wifi, mac_ble, mac_wifi, is_qualified, is_sync, datetime=None):
        self.device_type = device_type
        self.factory = factory
        self.fw_version = fw_version
        self.rssi_ble = rssi_ble
        self.rssi_wifi = rssi_wifi
        self.mac_ble = mac_ble
        self.mac_wifi = mac_wifi
        self.is_qualified = is_qualified
        self.is_sync = is_sync
        self.datetime = datetime
    def __init__(self, age_obj):
        self.device_type = age_obj.device_type
        self.factory = age_obj.factory
        self.fw_version = age_obj.fw_version
        self.rssi_ble = age_obj.rssi_ble
        self.rssi_wifi = age_obj.rssi_wifi
        self.mac_ble = age_obj.mac_ble
        self.mac_wifi = age_obj.mac_wifi
        self.is_qualified = age_obj.is_qualified
        self.is_sync = age_obj.is_sync
        self.datetime = age_obj.datetime
