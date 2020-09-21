from flask_sqlalchemy import SQLAlchemy
import datetime

from app.fcode import FCODE

# 1. lasy init
db_mysql = SQLAlchemy(use_native_unicode='utf8')

# 2. model definition


class Factory(db_mysql.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'factories'
    id = db_mysql.Column(db_mysql.Integer, nullable=False, autoincrement=True, primary_key = True)
    code = db_mysql.Column(db_mysql.Integer, nullable=False, unique=True)
    name = db_mysql.Column(db_mysql.String(100), unique=True, nullable=False)
    description = db_mysql.Column(db_mysql.Text)
    # devices = db_mysql.relationship('Device', backref='factory')
    testdatas = db_mysql.relationship('Testdata', backref='factory')
    testdatasarchive = db_mysql.relationship('TestdataArchive', backref='factory')
    def __init__(self, code, name, description=''):
        self.code = code
        self.name = name
        self.description = description
    @staticmethod
    def seed():
        f0 = Factory(0, 'All', '')
        f1 = Factory(1, 'Leedarson', '')
        f2 = Factory(2, 'Innotech', '')
        f3 = Factory(3, 'Tonly', '')
        f4 = Factory(4, 'Changhong', '')
        f5 = Factory(5, 'TestFactory', '')
        f6 = Factory(6, 'Topstar', '')
        db_mysql.session.add_all([f0, f1, f2, f3, f4, f5, f6])
        db_mysql.session.commit()


class Device(db_mysql.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'devices'
    id = db_mysql.Column(db_mysql.Integer, nullable=False, autoincrement=True, primary_key = True)
    code = db_mysql.Column(db_mysql.Integer, nullable=False, unique=True)
    name = db_mysql.Column('name', db_mysql.String(100), nullable=False)
    code_hex = db_mysql.Column(db_mysql.String(10), nullable=False, unique=True)
    # factorycode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(Factory.code), nullable=False)
    description = db_mysql.Column(db_mysql.Text, nullable=True)
    testdatas = db_mysql.relationship('Testdata', backref='device')
    testdatasarchive = db_mysql.relationship('TestdataArchive', backref='device')
    def __init__(self, code, code_hex, factorycode, name, description=''):
        self.code = code
        self.code_hex = code_hex
        self.factorycode = factorycode
        self.name = name
        self.description = description
    @staticmethod
    def seed():
        d_leedarson_09 = Device(9, '0x09', 1, 'Gen2 Tier2 C-Life Standalone')
        d_leedarson_11 = Device(11, '0x0B', 1, 'Gen2 Tier2 Sleep-BR30 Standalone')
        d_leedarson_13 = Device(13, '0x0D', 1, 'Gen2 TCO C-Life A19 ST')
        d_leedarson_27 = Device(27, '0x1B', 1, 'Gen2 TCO C-Life A19 MFG')
        d_leedarson_14 = Device(14, '0x0E', 1, 'Gen2 TCO C-Sleep A19 ST')
        d_leedarson_28 = Device(28, '0x1C', 1, 'Gen2 TCO C-Sleep A19 MFG')
        d_leedarson_15 = Device(15, '0x0F', 1, 'Gen2 TCO C-Sleep BR30 ST')
        d_leedarson_29 = Device(29, '0x1D', 1, 'Gen2 TCO C-Sleep BR30 MFG')
        d_leedarson_128 = Device(128, '0x80', 1, 'Dual mode Soft White A19', 'Leedarson, Topstar')
        d_leedarson_129 = Device(129, '0x81', 1, 'Dual mode Tunable White A19')
        d_leedarson_130 = Device(130, '0x82', 1, 'Dual mode Tunable White BR30')
        d_leedarson_67 = Device(67, '0x43', 1, 'Out door Plug')

        d_innotech_30 = Device(30, '0x1E', 2, 'Gen2 TCO Full Color A19 ST')
        d_innotech_31 = Device(31, '0x1F', 2, 'Gen2 TCO Full Color A19 MFG')
        d_innotech_32 = Device(32, '0x20', 2, 'Gen2 TCO Full Color BR30 ST')
        d_innotech_33 = Device(33, '0x21', 2, 'Gen2 TCO Full Color BR30 MFG')
        d_innotech_34 = Device(34, '0x22', 2, 'Gen2 TCO Full Color Strip ST')
        d_innotech_35 = Device(35, '0x23', 2, 'Gen2 TCO Full Color Strip MFG')
        d_innotech_131 = Device(131, '0x83', 2, 'Dual mode Full Color A19', 'Innotech, Leedarson')
        d_innotech_132 = Device(132, '0x84', 2, 'Dual mode Full Color BR30', 'Innotech, Leedarson')
        d_innotech_133 = Device(133, '0x85', 2, 'Dual mode Full Color Strip')
        d_innotech_48 = Device(48, '0x30', 2, 'Dimmer switch')
        d_innotech_49 = Device(49, '0x31', 2, 'Dimmer Switch(Premium)')
        d_innotech_51 = Device(51, '0x33', 2, 'Switch Paddle')
        d_innotech_52 = Device(52, '0x34', 2, 'Switch Toggle')
        d_innotech_53 = Device(53, '0x35', 2, 'Switch Centre Button')
        d_innotech_61 = Device(61, '0x3D', 2, 'Paddle switch TCO')
        d_innotech_62 = Device(62, '0x3E', 2, 'Toggle switch TCO')
        d_innotech_63 = Device(63, '0x3F', 2, 'Button switch TCO')
        d_innotech_65 = Device(65, '0x41', 2, 'GEN 1 Plug TCO')
    
        d_tonly_55 = Device(55, '0x37', 3, 'Dimmer Switch')
        d_tonly_56 = Device(56, '0x38', 3, 'Dimmer Switch(Premium)')
        d_tonly_57 = Device(58, '0x3A', 3, 'Switch Toggle')
        d_tonly_58 = Device(57, '0x39', 3, 'Switch Paddle')
        d_tonly_59 = Device(59, '0x3B', 3, 'Switch Centre Button')
        d_tonly_81 = Device(81, '0x51', 3, 'Fan Speed Switch')

        d_changhong_66 = Device(66, '0x42', 4, 'Indoor Plug GEN2')

        # same device id as d_leedarson_128
        # d_topstar_254 = Device(254, '0xFE', 6, 'Dual Mode Soft White Lamp(0x80)', 'Device ID 冲突')

        # todo
        d_test_255 = Device(255, '0xFF', 5, 'TestDevice')


        devices_all = [
            d_leedarson_09,
            d_leedarson_11,
            d_leedarson_13,
            d_leedarson_27,
            d_leedarson_14,
            d_leedarson_28,
            d_leedarson_15,
            d_leedarson_29,
            d_leedarson_128,
            d_leedarson_129,
            d_leedarson_130,
            d_leedarson_67,
            d_innotech_30,
            d_innotech_31,
            d_innotech_32,
            d_innotech_33,
            d_innotech_34,
            d_innotech_35,
            d_innotech_131,
            d_innotech_132,
            d_innotech_133,
            d_innotech_48,
            d_innotech_49,
            d_innotech_51,
            d_innotech_52,
            d_innotech_53,
            d_innotech_49,
            d_innotech_48,
            d_innotech_61,
            d_innotech_62,
            d_innotech_63,
            d_innotech_65,
            d_tonly_55,
            d_tonly_56,
            d_tonly_57,
            d_tonly_58,
            d_tonly_59,
            d_tonly_81,
            d_changhong_66,
            # d_topstar_254,
        ]

        devices_test = [d_test_255,]

        db_mysql.session.add_all(devices_all)
        db_mysql.session.add_all(devices_test)
        db_mysql.session.commit()



class Testdata(db_mysql.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'testdatas'
    id = db_mysql.Column(db_mysql.Integer, nullable=False, autoincrement=True, primary_key = True)
    # devicecode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey('devices.code'), nullable=False)
    # factorycode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey('factories.code'), nullable=True, server_default=str(FCODE))
    devicecode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(Device.code), nullable=False)
    factorycode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(Factory.code), nullable=True, server_default=str(FCODE))
    fw_version = db_mysql.Column(db_mysql.String(20))
    rssi_ble1 = db_mysql.Column(db_mysql.Integer)
    rssi_ble2 = db_mysql.Column(db_mysql.Integer)
    rssi_wifi1 = db_mysql.Column(db_mysql.Integer)
    rssi_wifi2 = db_mysql.Column(db_mysql.Integer)
    mac_ble = db_mysql.Column(db_mysql.String(18))
    mac_wifi = db_mysql.Column(db_mysql.String(18))
    status_cmd_check1 = db_mysql.Column(db_mysql.Integer, nullable=True)
    status_cmd_check2 = db_mysql.Column(db_mysql.Integer, nullable=True)
    bool_uploaded = db_mysql.Column(db_mysql.Boolean, server_default=str(0))
    bool_qualified_signal = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_check = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_scan = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_deviceid = db_mysql.Column(db_mysql.Boolean)
    datetime = db_mysql.Column(db_mysql.DateTime, default=datetime.datetime.now())
    # mac address check result
    reserve_int_1 = db_mysql.Column(db_mysql.Integer, nullable=True, server_default=str(0))
    # MCU version string
    reserve_str_1 = db_mysql.Column(db_mysql.String(100), nullable=True, server_default=str(''))
    # version check result success or not
    reserve_bool_1 = db_mysql.Column(db_mysql.Boolean, nullable=True, server_default=str(0))
    bool_qualified_overall = db_mysql.Column(db_mysql.Boolean, nullable=True, server_default=str(1))
    def __init__(self, devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, status_cmd_check1, status_cmd_check2, bool_uploaded, bool_qualified_signal, bool_qualified_check, bool_qualified_scan, bool_qualified_deviceid, datetime, reserve_str_1, reserve_bool_1, bool_qualified_overall):
        self.devicecode = devicecode
        self.factorycode = factorycode
        self.fw_version = fw_version
        self.rssi_ble1 = rssi_ble1
        self.rssi_ble2 = rssi_ble2
        self.rssi_wifi1 = rssi_wifi1
        self.rssi_wifi2 = rssi_wifi2
        self.mac_ble = mac_ble
        self.mac_wifi = mac_wifi
        self.datetime = datetime
        self.status_cmd_check1 = status_cmd_check1
        self.status_cmd_check2 = status_cmd_check2
        self.bool_uploaded = bool_uploaded
        self.bool_qualified_signal = bool_qualified_signal
        self.bool_qualified_check = bool_qualified_check
        self.bool_qualified_scan = bool_qualified_scan
        self.bool_qualified_deviceid = bool_qualified_deviceid
        self.datetime = datetime
        self.reserve_str_1 = reserve_str_1
        self.reserve_bool_1 = reserve_bool_1
        self.bool_qualified_overall = bool_qualified_overall
    @staticmethod
    def seed():
        pass


class TestdataStage(db_mysql.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'testdatasstage'
    id = db_mysql.Column(db_mysql.Integer, nullable=False, autoincrement=True, primary_key = True)
    devicecode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(Device.code), nullable=False)
    factorycode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(Factory.code), nullable=True)
    fw_version = db_mysql.Column(db_mysql.String(20))
    rssi_ble1 = db_mysql.Column(db_mysql.Integer)
    rssi_ble2 = db_mysql.Column(db_mysql.Integer)
    rssi_wifi1 = db_mysql.Column(db_mysql.Integer)
    rssi_wifi2 = db_mysql.Column(db_mysql.Integer)
    mac_ble = db_mysql.Column(db_mysql.String(18))
    mac_wifi = db_mysql.Column(db_mysql.String(18))
    status_cmd_check1 = db_mysql.Column(db_mysql.Integer)
    status_cmd_check2 = db_mysql.Column(db_mysql.Integer)
    bool_uploaded = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_signal = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_check = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_scan = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_deviceid = db_mysql.Column(db_mysql.Boolean)
    # datetime = db_mysql.Column(db_mysql.DateTime, default=datetime.datetime.now())
    # reserve_int_1 = db_mysql.Column(db_mysql.Integer, nullable=True, server_default=str(0))
    # reserve_str_1 = db_mysql.Column(db_mysql.String(100), nullable=True, server_default=str(''))
    # reserve_bool_1 = db_mysql.Column(db_mysql.Boolean, nullable=True, server_default=str(0))
    datetime = db_mysql.Column(db_mysql.DateTime)
    reserve_int_1 = db_mysql.Column(db_mysql.Integer)
    reserve_str_1 = db_mysql.Column(db_mysql.String(100))
    reserve_bool_1 = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_overall = db_mysql.Column(db_mysql.Boolean)
    def __init__(self, devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, status_cmd_check1, status_cmd_check2, bool_uploaded, bool_qualified_signal, bool_qualified_check, bool_qualified_scan, bool_qualified_deviceid, datetime, reserve_int_1, reserve_str_1, reserve_bool_1, bool_qualified_overall):
        self.devicecode = devicecode
        self.factorycode = factorycode
        self.fw_version = fw_version
        self.rssi_ble1 = rssi_ble1
        self.rssi_ble2 = rssi_ble2
        self.rssi_wifi1 = rssi_wifi1
        self.rssi_wifi2 = rssi_wifi2
        self.mac_ble = mac_ble
        self.mac_wifi = mac_wifi
        self.status_cmd_check1 = status_cmd_check1
        self.status_cmd_check2 = status_cmd_check2
        self.bool_uploaded = bool_uploaded
        self.bool_qualified_signal = bool_qualified_signal
        self.bool_qualified_check = bool_qualified_check
        self.bool_qualified_scan = bool_qualified_scan
        self.bool_qualified_deviceid = bool_qualified_deviceid
        self.datetime = datetime
        self.reserve_int_1 = reserve_int_1
        self.reserve_str_1 = reserve_str_1
        self.reserve_bool_1 = reserve_bool_1
        self.bool_qualified_overall = bool_qualified_overall


class TestdataArchive(db_mysql.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'testdatasarchive'
    id = db_mysql.Column(db_mysql.Integer, nullable=False, autoincrement=True, primary_key = True)
    devicecode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(Device.code), nullable=False)
    # factorycode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(Factory.code), nullable=True, server_default=str(FCODE))
    factorycode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(Factory.code), nullable=True)
    fw_version = db_mysql.Column(db_mysql.String(20))
    rssi_ble1 = db_mysql.Column(db_mysql.Integer)
    rssi_ble2 = db_mysql.Column(db_mysql.Integer)
    rssi_wifi1 = db_mysql.Column(db_mysql.Integer)
    rssi_wifi2 = db_mysql.Column(db_mysql.Integer)
    mac_ble = db_mysql.Column(db_mysql.String(18))
    mac_wifi = db_mysql.Column(db_mysql.String(18))
    status_cmd_check1 = db_mysql.Column(db_mysql.Integer)
    status_cmd_check2 = db_mysql.Column(db_mysql.Integer)
    bool_uploaded = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_signal = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_check = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_scan = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_deviceid = db_mysql.Column(db_mysql.Boolean)
    # datetime = db_mysql.Column(db_mysql.DateTime, default=datetime.datetime.now())
    # reserve_int_1 = db_mysql.Column(db_mysql.Integer, nullable=True, server_default=str(0))
    # reserve_str_1 = db_mysql.Column(db_mysql.String(100), nullable=True, server_default=str(''))
    # reserve_bool_1 = db_mysql.Column(db_mysql.Boolean, nullable=True, server_default=str(0))
    datetime = db_mysql.Column(db_mysql.DateTime)
    reserve_int_1 = db_mysql.Column(db_mysql.Integer)
    reserve_str_1 = db_mysql.Column(db_mysql.String(100))
    reserve_bool_1 = db_mysql.Column(db_mysql.Boolean)
    bool_qualified_overall = db_mysql.Column(db_mysql.Boolean)
    def __init__(self, devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, status_cmd_check1, status_cmd_check2, bool_uploaded, bool_qualified_signal, bool_qualified_check, bool_qualified_scan, bool_qualified_deviceid, datetime, reserve_int_1, reserve_str_1, reserve_bool_1, bool_qualified_overall):
        self.devicecode = devicecode
        self.factorycode = factorycode
        self.fw_version = fw_version
        self.rssi_ble1 = rssi_ble1
        self.rssi_ble2 = rssi_ble2
        self.rssi_wifi1 = rssi_wifi1
        self.rssi_wifi2 = rssi_wifi2
        self.mac_ble = mac_ble
        self.mac_wifi = mac_wifi
        self.status_cmd_check1 = status_cmd_check1
        self.status_cmd_check2 = status_cmd_check2
        self.bool_uploaded = bool_uploaded
        self.bool_qualified_signal = bool_qualified_signal
        self.bool_qualified_check = bool_qualified_check
        self.bool_qualified_scan = bool_qualified_scan
        self.bool_qualified_deviceid = bool_qualified_deviceid
        self.datetime = datetime
        self.reserve_int_1 = reserve_int_1
        self.reserve_str_1 = reserve_str_1
        self.reserve_bool_1 = reserve_bool_1
        self.bool_qualified_overall = bool_qualified_overall

