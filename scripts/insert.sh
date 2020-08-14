#! /usr/bin/env bash
#
for i in $(seq 1 10000); do
  mysql -p123456 -e "INSERT ge.testdatasarchive(devicecode, factorycode, fw_version, rssi_ble1, rssi_ble2, rssi_wifi1, rssi_wifi2, mac_ble, mac_wifi, status_cmd_check1, status_cmd_check2, bool_qualified_signal, bool_qualified_check, bool_qualified_scan, bool_qualified_deviceid, datetime, reserve_str_1, reserve_bool_1) VALUES(128, 1, '3.1', -65, -65, -33, -33, 'f4bcda704c20', '010203040506', 11111, 11111, true, true, true, true, now(), '222', true)"
done
