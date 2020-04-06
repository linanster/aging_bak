from app.models import db, Testdata, TestdataArchive

def testdatas_archive():
    testdatas_list = Testdata.query.all()
    testdatasarchive_list = list()
    for item in testdatas_list:
        devicecode = item.devicecode
        factorycode = item.factorycode
        fw_version = item.fw_version
        rssi_ble = item.rssi_ble
        rssi_wifi = item.rssi_wifi
        mac_ble = item.mac_ble
        mac_wifi = item.mac_wifi
        is_qualified = item.is_qualified
        is_sync = item.is_sync
        datetime = item.datetime        
        obj = TestdataArchive(devicecode, factorycode, fw_version, rssi_ble, rssi_wifi, mac_ble, mac_wifi, is_qualified, is_sync, datetime)
        testdatasarchive_list.append(obj)
    db.session.add_all(testdatasarchive_list)
    db.session.commit()

def testdata_upload():
    pass
