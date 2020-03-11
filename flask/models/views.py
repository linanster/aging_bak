from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy(use_native_unicode='utf8')

def init_views(app):
    db.init_app(app)

class view_data_aging(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key = True)
    device_type = db.Column(db.String(100))
    factory = db.Column(db.String(100))
    fw_version = db.Column(db.String(100))
    rssi_ble = db.Column(db.Integer)
    rssi_wifi = db.Column(db.Integer)
    mac_ble = db.Column(db.String(100))
    mac_wifi = db.Column(db.String(100))
    is_qualified = db.Column(db.Boolean)
    is_sync = db.Column(db.Boolean)
    datetime = db.Column(db.Time, default=datetime.datetime.now())

def query_aging_all_from_view():
    return view_data_aging.query.all()
