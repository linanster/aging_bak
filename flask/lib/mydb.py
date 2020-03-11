#! /usr/bin/env python3
# coding: utf8
#
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime


# 1. lasy init
db = SQLAlchemy(use_native_unicode='utf8')
db2 = SQLAlchemy(use_native_unicode='utf8')

def init_model(app):
    db.init_app(app)
    db2.init_app(app)


# 2. model definition

class tb_device_type(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    type = db.Column('type', db.String(100), nullable=False)
    detail = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    def __init__(self, code, type, detail, description=None):
        self.code = code
        self.type = type
        self.detail = detail
        self.description = description


class tb_factory(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    def __init__(self, id, name, description=None):
        self.id = id
        self.name = name
        self.description = description

class tb_data_aging(db.Model):
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
    datetime = db.Column(db.Time, default=datetime.datetime.now())
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

class view_data_aging(db2.Model):
    id = db2.Column(db2.Integer, nullable=False, autoincrement=True, primary_key = True)
    device_type = db2.Column(db2.String(100))
    factory = db2.Column(db2.String(100))
    fw_version = db2.Column(db2.String(100))
    rssi_ble = db2.Column(db2.Integer)
    rssi_wifi = db2.Column(db2.Integer)
    mac_ble = db2.Column(db2.String(100))
    mac_wifi = db2.Column(db2.String(100))
    is_qualified = db2.Column(db2.Boolean)
    is_sync = db2.Column(db2.Boolean)
    datetime = db2.Column(db2.Time, default=datetime.datetime.now())


# 3. CRUD functions

def create_tables():
    db.create_all()

def delete_tables():
    db.drop_all()
    

def query_aging_all():
    return tb_data_aging.query.all()

def query_device_all():
    return tb_device_type.query.all()

def query_factory_all():
    return tb_factory.query.all()

def query_aging_all_from_view():
    return view_data_aging.query.all()

def gen_testdata():
    d1 = tb_device_type(1, 'C-Life', 'Gen1/Gen2 ST C-Life(Ox01)')
    d2 = tb_device_type(17, 'C-Life', 'Gen2 Andromeda C-Life(0x11)')
    d3 = tb_device_type(18, 'C-Life', 'Gen2 MFG C-Life(0x12)')
    d4 = tb_device_type(5, 'C-Sleep', 'Gen1/Gen2 ST C-Sleep(0x05)')
    d5 = tb_device_type(19, 'C-Sleep', 'Gen2 MFG C-Sleep(0x13)')
    f1 = tb_factory(1, 'Leedarson', '立达信')
    f2 = tb_factory(2, 'Innotech', 'Smart LED Light Bulbs')
    f3 = tb_factory(3, 'Tonly', '通力')
    a1 = tb_data_aging(5, 2, '3.1', -65, -33, 'd74d38dabcf1', '88:50:F6:04:62:31', True, False)
    a2 = tb_data_aging(1, 3, '3.2', -65, -33, 'd74d38dabcf5', '88:50:F6:04:62:35', True, False)
    a3 = tb_data_aging(17, 1, '3.40', -65, -33, 'd74d38dabcf7', '88:50:F6:04:62:37', True, False)
    
    datas = [d1, d2, d3, d4, d5, f1, f2, f3]
    for data in datas:
        db.session.add(data)
    db.session.commit()
    datas = [a1, a2, a3]
    for data in datas:
        db.session.add(data)
    db.session.commit()

