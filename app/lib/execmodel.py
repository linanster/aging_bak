from app.models import db_mysql, Testdata, TestdataStage, TestdataArchive
from app.lib.mylogger import logger_app

def testdatas_cleanup():
    try:
        Testdata.query.delete()
    except Exception as e:
        raise e
        db_mysql.session.rollback()
    else:
        db_mysql.session.commit()

def testdatasstage_cleanup():
    try:
        TestdataStage.query.delete()
    except Exception as e:
        raise e
        db_mysql.session.rollback()
    else:
        db_mysql.session.commit()

def testdatasarchive_cleanup():
    try:
        count = TestdataArchive.query.delete()
    except Exception as e:
        raise e
        db_mysql.session.rollback()
    else:
        db_mysql.session.commit()
    finally:
        return count


def testdatasarchive_cleanup_legacy():
    try:
        # TestdataArchive.query.delete()
        count = TestdataArchive.query.filter_by(bool_uploaded=True).delete(synchronize_session=False)
    except Exception as e:
        logger_app.error('[testdatasarchive_cleanup]:')
        logger_app.error(str(e))
        db_mysql.session.rollback()
        return -1
    else:
        db_mysql.session.commit()
        return count


# copy data from testdatas to testdatasstage table
def testdatas_stage():
    testdatas_list = Testdata.query.all()
    testdatasstage_list = list()
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
        obj = TestdataStage(devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, status_cmd_check1, status_cmd_check2, bool_uploaded, bool_qualified_signal, bool_qualified_check, bool_qualified_scan, bool_qualified_deviceid, datetime, reserve_int_1, reserve_str_1, reserve_bool_1)
        testdatasstage_list.append(obj)
    db_mysql.session.add_all(testdatasstage_list)
    db_mysql.session.commit()


# copy data from testdatasstage to testdatasarchive table
def testdatas_archive():
    testdatas_list = TestdataStage.query.all()
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
    db_mysql.session.add_all(testdatasarchive_list)
    db_mysql.session.commit()


def update_testdatas_fcode(fcode):
    datas_raw = Testdata.query.all()
    try:
        for item in datas_raw:
            item.factorycode = fcode
            db_mysql.session.add(item)
    except Exception as e:
        db_mysql.session.rollback()
        # logger_app.error('update_testdatas_fcode:')
        # logger_app.error(str(e))
        # return 4
    else:
        db_mysql.session.commit()
        # logger_app.info('update_testdatas_fcode: success(count: {})'.format(len(datas_raw)))
        # return 0


def update_testdatas_devicecode(dcode):
    datas_raw = Testdata.query.all()
    try:
        for item in datas_raw:
            item.devicecode = dcode
            db_mysql.session.add(item)
    except Exception as e:
        db_mysql.session.rollback()
        # logger_app.error('update_testdatas_devicecode:')
        # logger_app.error(str(e))
        # return 4
    else:
        db_mysql.session.commit()
        # logger_app.info('update_testdatas_devicecode: success(count: {})'.format(len(datas_raw)))
        # return 0
