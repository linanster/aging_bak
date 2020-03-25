from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime


# 1. lasy init
db = SQLAlchemy(use_native_unicode='utf8')

class RunningState(db.Model):
    __bind_key__ = 'sqlite'
    __tablename__ = 'runningstates'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    metric = db.Column(db.String(100))
    state = db.Column(db.Boolean)
    description = db.Column(db.String(100))
    def __init__(self, metric, state=False, description=''):
        self.metric = metric
        self.state = state
        self.description = description
    @staticmethod
    def seed():
        s_stopped = RunningState('s_stopped', True, 'Indicate stopped or not, default is True.')
        a_stop = RunningState('a_stop', False, 'Indicate if stop command send out, default is False.')
        s_paused = RunningState('s_paused', False, 'Indicate paused or not, default is False')
        a_pause = RunningState('a_pause', False, 'Indicate if pause commend send out, default is False')
        db.session.add_all([s_stopped, a_stop, s_paused, a_pause])
        db.session.commit()

# 2. model definition

class Device(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'devices'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    type = db.Column('type', db.String(100), nullable=False)
    detail = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    Testdata = db.relationship('Testdata', backref='Device')
    def __init__(self, code, type, detail, description=''):
        self.code = code
        self.type = type
        self.detail = detail
        self.description = description
    @staticmethod
    def seed():
        d1 = Device(1, 'C-Life', 'Gen1/Gen2 ST C-Life(Ox01)')
        d2 = Device(17, 'C-Life', 'Gen2 Andromeda C-Life(0x11)')
        d3 = Device(18, 'C-Life', 'Gen2 MFG C-Life(0x12)')
        d4 = Device(5, 'C-Sleep', 'Gen1/Gen2 ST C-Sleep(0x05)')
        d5 = Device(19, 'C-Sleep', 'Gen2 MFG C-Sleep(0x13)')
        db.session.add_all([d1, d2, d3, d4, d5])
        db.session.commit()

class Factory(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'factories'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    Testdata = db.relationship('Testdata', backref='Factory')
    def __init__(self, code, name, description=''):
        self.code = code
        self.name = name
        self.description = description
    @staticmethod
    def seed():
        f1 = Factory(1, 'Leedarson', '立达信')
        f2 = Factory(2, 'Innotech', 'Smart LED Light Bulbs')
        f3 = Factory(3, 'Tonly', '通力')
        db.session.add_all([f1, f2, f3])
        db.session.commit()

class Testdata(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'testdatas'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    device_type = db.Column(db.Integer, db.ForeignKey('devices.code'), nullable=False)
    factory = db.Column(db.Integer, db.ForeignKey('factories.code'), nullable=False) 
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
        a1 = Testdata(5, 2, '3.1', -65, -33, 'd74d38dabcf1', '88:50:F6:04:62:31', True, False, datetime.datetime.now())
        a2 = Testdata(1, 3, '3.2', -65, -33, 'd74d38dabcf5', '88:50:F6:04:62:35', True, False, datetime.datetime.now())
        a3 = Testdata(17, 1, '3.40', -65, -33, 'd74d38dabcf7', '88:50:F6:04:62:37', False, False, datetime.datetime.now())
        db.session.add_all([a1, a2, a3])
        db.session.commit()

