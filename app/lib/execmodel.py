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
        is_qualified = item.is_qualified
        is_sync = item.is_sync
        datetime = item.datetime        
        status_cmd_check1 = item.status_cmd_check1
        status_cmd_check2 = item.status_cmd_check2
        obj = TestdataArchive(devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, is_qualified, is_sync, datetime, status_cmd_check1, status_cmd_check2)
        testdatasarchive_list.append(obj)
    db.session.add_all(testdatasarchive_list)
    db.session.commit()

def testdata_upload():
    pass
