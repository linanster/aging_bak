-- 0 clean up
DROP VIEW IF EXISTS getest.view_students;
DROP TABLE IF EXISTS getest.tb_students;
DROP TABLE IF EXISTS getest.tb_courses;
DROP DATABASE IF EXISTS getest;

-- 1.1 创建数据库getest
CREATE DATABASE IF NOT EXISTS getest DEFAULT CHARACTER SET utf8;

-- 1.2 切换到数据库getest
USE getest;


-- 2 创建表：

-- 2.1 主表 courses
CREATE TABLE IF NOT EXISTS tb_courses(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code INT UNSIGNED UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    credit TINYINT NOT NULL, 
    description TINYTEXT
)
CHARACTER SET utf8;

-- 2.2 从表 student
CREATE TABLE IF NOT EXISTS tb_students(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course_code INT UNSIGNED NOT NULL,
    age INT UNSIGNED,
    CONSTRAINT fk_course_code FOREIGN KEY(course_code) REFERENCES tb_courses(code)
    ON UPDATE CASCADE ON DELETE CASCADE
)
CHARACTER SET utf8;

-- 2.4 创建视图view_students
CREATE VIEW view_students AS 
    SELECT
        s.name AS "name",
        s.age,
        c.name AS "curse"
    FROM tb_students AS s, tb_courses AS c
    WHERE s.course_code=c.code;

-- 2.5 验证
SHOW TABLES;

-- 3 写入初始化数据

-- 3.1 清空表
DELETE FROM getest.tb_students;
DELETE FROM getest.tb_courses;

-- 3.2 插入表tb_courses 模拟数据
INSERT INTO getest.tb_courses(name, code, credit, description) VALUES
    ('Chinese', 1, 10, '语文课,学分10'),
    ('English', 2, 8, '英语课,学分8'),
    ('History', 3, 5, '历史课,学分5')
;


-- 3.4 插入表tb_data_aging 模拟数据
INSERT INTO getest.tb_students(name, course_code, age) VALUES
    ('Jun', 3, 33),
    ('Nan', 1, 32),
    ('Allen', 2, 29)
;

-- 2.1 验证
SELECT * FROM getest.view_students;
