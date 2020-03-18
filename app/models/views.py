from flask_sqlalchemy import SQLAlchemy
import datetime

view = SQLAlchemy(use_native_unicode='utf8')

class view_data_aging(view.Model):
    __bind_key__ = 'main'
    __tablename__ = 'view_data_aging'
    id = view.Column(view.Integer, nullable=False, autoincrement=True, primary_key = True)
    device_type = view.Column(view.String(100))
    factory = view.Column(view.String(100))
    fw_version = view.Column(view.String(100))
    rssi_ble = view.Column(view.Integer)
    rssi_wifi = view.Column(view.Integer)
    mac_ble = view.Column(view.String(100))
    mac_wifi = view.Column(view.String(100))
    is_qualified = view.Column(view.Boolean)
    is_sync = view.Column(view.Boolean)
    datetime = view.Column(view.DateTime, default=datetime.datetime.now())



