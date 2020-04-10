-- 1. 删除数据库ge
DROP DATABASE IF EXISTS ge;

-- 2. 创建数据库ge
CREATE DATABASE IF NOT EXISTS ge DEFAULT CHARACTER SET utf8;

-- 3. 初始化表
-- 这部分代码在flask manage.py中完成
-- python3 manage.py init
-- python3 manage.py createdb
