from app.models import db, Testdata, TestdataArchive

def testdatas_archive():
    testdatas_list = Testdata.query.all()
    testdatasarchive_list = list()
    for item in testdatas_list:
        devicecode = item.devicecode
        factorycode = item.factorycode
        fw_version = item.fw_version
        rssi_ble1 = item.rssi_ble1
        rssi_ble2 = item.rssi_ble2
        rssi_wifi1 = item.rssi_wifi1
        rssi_wifi2 = item.rssi_wifi2
        mac_ble = item.mac_ble
        mac_wifi = item.mac_wifi
        status_cmd_check1 = item.status_cmd_check1
        status_cmd_check2 = item.status_cmd_check2
        bool_uploaded = item.bool_uploaded
        bool_qualified_signal = item.bool_qualified_signal
        bool_qualified_check = item.bool_qualified_check
        bool_qualified_scan = item.bool_qualified_scan
        bool_qualified_deviceid = item.bool_qualified_deviceid
        datetime = item.datetime
        reserve_int_1 = item.reserve_int_1
        reserve_str_1 = item.reserve_str_1
        reserve_bool_1 = item.reserve_bool_1
        obj = TestdataArchive(devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, status_cmd_check1, status_cmd_check2, bool_uploaded, bool_qualified_signal, bool_qualified_check, bool_qualified_scan, bool_qualified_deviceid, datetime, reserve_int_1, reserve_str_1, reserve_bool_1)
        testdatasarchive_list.append(obj)
    db.session.add_all(testdatasarchive_list)
    db.session.commit()

def testdata_upload():
    pass
