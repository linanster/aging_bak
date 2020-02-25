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

-- 2.2 主表 tb_factory
CREATE TABLE IF NOT EXISTS tb_factory(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL, 
    description TINYTEXT
)
CHARACTER SET utf8;

-- 2.3 从表 tb_data_aging
CREATE TABLE IF NOT EXISTS tb_data_aging(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    device_type INT UNSIGNED NOT NULL,
    factory INT UNSIGNED NOT NULL,
    fw_version VARCHAR(20),
    rssi_ble TINYINT NOT NULL,
    rssi_wifi TINYINT,
    mac_ble VARCHAR(12) NOT NULL,
    mac_wifi VARCHAR(17),
    is_qualified BOOLEAN,
    is_sync BOOLEAN,
    datetime DATETIME,
    CONSTRAINT fk_device_type FOREIGN KEY(device_type) REFERENCES tb_device_type(code)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_factory FOREIGN KEY (factory) REFERENCES tb_factory(id)
    ON UPDATE CASCADE ON DELETE CASCADE    
)
CHARACTER SET utf8;

-- 3.4 创建视图view_data_aging
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

-- 3 验证
SHOW TABLES;
