from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime


# 1. lasy init
db = SQLAlchemy(use_native_unicode='utf8')

def init_tables(app):
    db.init_app(app)

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

