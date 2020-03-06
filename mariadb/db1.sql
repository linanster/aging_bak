-- 0 clean up
DROP VIEW IF EXISTS ge.view_data_aging;
DROP TABLE IF EXISTS ge.tb_data_aging;
DROP TABLE IF EXISTS ge.tb_device_type;
DROP TABLE IF EXISTS ge.tb_factory;
DROP DATABASE IF EXISTS ge;

-- 1.1 创建数据库ge
CREATE DATABASE IF NOT EXISTS ge DEFAULT CHARACTER SET utf8;

-- 1.2 切换到数据库ge
USE ge;


-- 2 创建表：

-- 2.1 主表 tb_device_type
CREATE TABLE IF NOT EXISTS tb_device_type(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code INT UNSIGNED UNIQUE NOT NULL,
    type VARCHAR(100) NOT NULL,
    detail VARCHAR(100) NOT NULL, 
    description TINYTEXT
)
CHARACTER SET utf8;
-- INSERT INTO tb_device_type SET code = 31, type = "device type 0x31", detail = "one type of bulb, test example1", description = "tinytext example1";
-- INSERT INTO tb_device_type SET code = 32, type = "device type 0x32", detail = "one type of bulb, test example2", description = "tinytext example2";

-- 2.2 主表 tb_factory
CREATE TABLE IF NOT EXISTS tb_factory(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL, 
    description TINYTEXT
)
CHARACTER SET utf8;
-- INSERT INTO tb_factory SET name = "innotech", description = "tinytext example1";
-- INSERT INTO tb_factory SET name = "tonly", description = "tinytext example2";

-- 2.3 从表 tb_data_aging
CREATE TABLE IF NOT EXISTS tb_data_aging(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    device_type INT UNSIGNED NOT NULL,
    factory INT UNSIGNED NOT NULL,
    fw_version VARCHAR(20),
    rssi_ble INT NOT NULL,
    rssi_wifi INT,
    mac_ble VARCHAR(18) NOT NULL,
    mac_wifi VARCHAR(18),
    is_qualified BOOLEAN,
    is_sync BOOLEAN,
    datetime DATETIME,
    CONSTRAINT fk_device_type FOREIGN KEY(device_type) REFERENCES tb_device_type(code)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_factory FOREIGN KEY (factory) REFERENCES tb_factory(id)
    ON UPDATE CASCADE ON DELETE CASCADE    
)
CHARACTER SET utf8;

-- 2.4 创建视图view_data_aging
CREATE VIEW view_data_aging AS 
    SELECT a.id AS "id", 
        d.type AS "device_type", 
        f.name AS 'factory', 
        a.fw_version,
        a.rssi_ble,
        a.rssi_wifi,
        a.mac_ble,
        a.mac_wifi,
        a.is_qualified,
        a.is_sync,
        a.datetime 
    FROM tb_data_aging AS a, tb_device_type AS d, tb_factory AS f 
    WHERE a.device_type=d.code AND a.factory=f.id;

-- 2.5 验证
SHOW TABLES;

-- 3 写入初始化数据

-- 3.1 清空表
DELETE FROM ge.tb_device_type;
DELETE FROM ge.tb_factory;
DELETE FROM ge.tb_data_aging;

-- 3。2 插入表tb_device_type 模拟数据
INSERT INTO ge.tb_device_type(code, type, detail, description) VALUES
    (1, 'C-Life', 'Gen1/Gen2 ST C-Life(Ox01)', null),
    (17, 'C-Life', 'Gen2 Andromeda C-Life(0x11)', null),
    (18, 'C-Life', 'Gen2 MFG C-Life(0x12)', null),
    (5, 'C-Sleep', 'Gen1/Gen2 ST C-Sleep(0x05)', null),
    (19, 'C-Sleep', 'Gen2 MFG C-Sleep(0x13)', null)
;


-- 3.3 插入表tb_factory 模拟数据
INSERT INTO ge.tb_factory(id, name, description) VALUES
    (1, 'Leedarson', '立达信'),
    (2, 'Innotech', 'Smart LED Light Bulbs'),
    (3, 'Tonly', '通力')
;


-- 3.4 插入表tb_data_aging 模拟数据
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
