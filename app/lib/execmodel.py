from app.models import db_mysql, Testdata, TestdataStage, TestdataArchive
from app.lib.mylogger import logger_app
from sqlalchemy import or_

def get_count_stage_uploaded_true():
    return len(TestdataStage.query.filter_by(bool_uploaded=True).all())

def get_count_stage_uploaded_false():
    return len(TestdataStage.query.filter_by(bool_uploaded=False).all())

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


def testdatasstage_cleanup_archived():
    # TestdataArchive.query.delete()
    count = TestdataStage.query.filter_by(bool_uploaded=True).delete(synchronize_session=False)


# copy data from testdatas to testdatasstage table
def testdatas_stage():
    try:
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
            bool_qualified_overall = item.bool_qualified_overall
            obj = TestdataStage(devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, status_cmd_check1, status_cmd_check2, bool_uploaded, bool_qualified_signal, bool_qualified_check, bool_qualified_scan, bool_qualified_deviceid, datetime, reserve_int_1, reserve_str_1, reserve_bool_1, bool_qualified_overall)
            testdatasstage_list.append(obj)
        db_mysql.session.add_all(testdatasstage_list)

    except Exception as e:
        logger_app.error('testdatas_stage:')
        logger_app.error(str(e))
    else:
        db_mysql.session.commit()


# copy data from testdatasstage to testdatasarchive table
def testdatasstage_archive():
    # testdatas_list = TestdataStage.query.all()
    testdatas_list = TestdataStage.query.filter_by(bool_uploaded=True).all()
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
        bool_qualified_overall = item.bool_qualified_overall
        obj = TestdataArchive(devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, status_cmd_check1, status_cmd_check2, bool_uploaded, bool_qualified_signal, bool_qualified_check, bool_qualified_scan, bool_qualified_deviceid, datetime, reserve_int_1, reserve_str_1, reserve_bool_1, bool_qualified_overall)
        testdatasarchive_list.append(obj)
    db_mysql.session.add_all(testdatasarchive_list)
    return len(testdatasarchive_list)
    # db_mysql.session.commit()


def update_testdatas_fcode(fcode):
    datas_raw = Testdata.query.all()
    try:
        for item in datas_raw:
            item.factorycode = fcode
            # db_mysql.session.add(item)
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
            # db_mysql.session.add(item)
    except Exception as e:
        db_mysql.session.rollback()
        # logger_app.error('update_testdatas_devicecode:')
        # logger_app.error(str(e))
        # return 4
    else:
        db_mysql.session.commit()
        # logger_app.info('update_testdatas_devicecode: success(count: {})'.format(len(datas_raw)))
        # return 0

def update_testdatas_bool_qualified_overall_legacy():
    datas = Testdata.query.filter(
        or_(
            Testdata.bool_qualified_signal == False,
            Testdata.bool_qualified_check == False,
            Testdata.bool_qualified_scan == False,
            Testdata.bool_qualified_deviceid == False,
            Testdata.reserve_bool_1 == False,
        )
    ).all()
    try:
        for data in datas:
            data.bool_qualified_overall = False
        # db_mysql.session.add_all(datas)
    except Exception as e:
        db_mysql.session.rollback()
        logger_app.error('update_testdatas_bool_qualified_overall:')
        logger_app.error(str(e))
    else:
        db_mysql.session.commit()

def update_testdatas_bool_qualified_overall():
    try:
        # datas = Testdata.query.filter(Testdata.bool_qualified_overall==None).all()
        # datas = Testdata.query.filter(Testdata.bool_qualified_overall==True).all()
        # datas = Testdata.query.filter(Testdata.bool_qualified_overall==False).all()
        datas = Testdata.query.all()
        for data in datas:
            if data.bool_qualified_signal and data.bool_qualified_check and data.bool_qualified_scan and data.bool_qualified_deviceid and data.reserve_bool_1 and data.reserve_int_1 == 0:
                data.bool_qualified_overall = True
            else:
                data.bool_qualified_overall = False

    except Exception as e:
        db_mysql.session.rollback()
        logger_app.error('update_testdatas_bool_qualified_overall:')
        logger_app.error(str(e))
    else:
        db_mysql.session.commit()
