# 1. 基础组件安装

## 1.1 CentOS
安装python3:<br/>
yum install python36 python36-pip python3-devel gcc<br/>
安装mariadb:<br/>
yum install mariadb mariadb-server mariadb-devel mariadb-libs<br/>
## 1.2 Rasp
安装python3:<br/>
apt install python3.6 python3.6-dev python3-pip
安装mariadb:<br/>

# 2. 组件初始化配置
## 2.1 mariadb环境
- 设置root密码<br/>
delete from mysql.user where user='root' and host not like 'localhost';<br/>
select * from mysql.user where user='root';<br/>
update mysql.user set password=PASSWORD('123456'),host='%' where user='root' and host='localhost';<br/>
flush privileges;<br/>
- 生成表结构<br/>
mysql -uroot -hlocalhost -p'123456' < mariadb/db1.sql<br/>
- 导入测试数据<br/>
mysql -uroot -hlocalhost -p'123456' < mariadb/db2.sql<br/>
## 2.2 python3环境
- pip安装python3第三方开发包<br/>
pip3 install flask flask-script flask-blueprint flask-sqlalchemy flask-migrate flask-session<br/>
pip3 install **pymysql**<br/>


# 3 笔记
连接数据库<br/>
mysql -hlocalhost -uroot -p123456 ge<br/>
其他<br/>
SHOW TABLE STATUS LIKE "%data_aging%";<br/>
SHOW CREATE DATABASE ge;<br/>
SHOW CREATE TABLE tb_data_aging;<br/>
