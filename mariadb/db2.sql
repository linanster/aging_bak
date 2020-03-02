-- 0 清空表
DELETE FROM ge.tb_device_type;
DELETE FROM ge.tb_factory;
DELETE FROM ge.tb_data_aging;

-- 1.1 插入表tb_device_type 模拟数据
INSERT INTO ge.tb_device_type(code, type, detail, description) VALUES
    (1, 'C-Life', 'Gen1/Gen2 ST C-Life(Ox01)', null),
    (17, 'C-Life', 'Gen2 Andromeda C-Life(0x11)', null),
    (18, 'C-Life', 'Gen2 MFG C-Life(0x12)', null),
    (5, 'C-Sleep', 'Gen1/Gen2 ST C-Sleep(0x05)', null),
    (19, 'C-Sleep', 'Gen2 MFG C-Sleep(0x13)', null)
;


-- 1.2 插入表tb_factory 模拟数据
INSERT INTO ge.tb_factory(id, name, description) VALUES
    (1, 'Leedarson', '立达信'),
    (2, 'Innotech', 'Smart LED Light Bulbs'),
    (3, 'Tonly', '通力')
;


-- 1.3 插入表tb_data_aging 模拟数据
INSERT INTO ge.tb_data_aging(device_type, factory, fw_version, rssi_ble, rssi_wifi, mac_ble, mac_wifi, is_qualified, is_sync, datetime) VALUES
    (5, 2, '3.1', -65, -33, 'd74d38dabcf1', '88:50:F6:04:62:31', true, false, now()),
    (5, 2, '3.1', -65, -33, 'd74d38dabcf2', '88:50:F6:04:62:32', true, false, now()),
    (5, 2, '3.1', -65, -33, 'd74d38dabcf3', '88:50:F6:04:62:33', true, false, now()),
    (5, 2, '3.2', -65, -33, 'd74d38dabcf4', '88:50:F6:04:62:34', true, false, now()),
    (1, 3, '3.2', -65, -33, 'd74d38dabcf5', '88:50:F6:04:62:35', true, false, now()),
    (1, 3, '3.1', -65, -33, 'd74d38dabcf6', '88:50:F6:04:62:36', true, false, now()),
    (17, 1, '3.40', -65, -33, 'd74d38dabcf7', '88:50:F6:04:62:37', true, false, now()),
    (17, 1, '3.41', -65, -33, 'd74d38dabcf8', '88:50:F6:04:62:38', true, false, now()),
    (17, 1, '3.4', -65, -33, 'd74d38dabcf9', '88:50:F6:04:62:39', true, false, now()),
    (17, 1, '3.41', -65, -33, 'd74d38dabcfa', '88:50:F6:04:62:3a', true, false, now())
;

-- 2.1 验证
SELECT * FROM ge.tb_device_type;
SELECT * FROM ge.tb_factory;
SELECT * FROM ge.tb_data_aging;

