# 1. 项目描述
老化测试平台代码，包括：
- Web服务器：Flask
- 数据库：Mariadb


# 2. Flask安装及配置

## 2.1 安装python3
CentOS: yum install python36 python36-pip python3-devel gcc<br/>
RaspPI: <br/>

## 2.2 安装python3第三方开发包
pip3 install flask flask-script flask-blueprint flask-sqlalchemy flask-migrate flask-session<br/>
pip3 install **pymysql**<br/>
pip2 install **MySQL-python**<br/>

## 2.3 其他

# 3. Mariadb安装及配置
## 3.1 安装数据库
CentOS: yum install mariadb mariadb-server mariadb-devel mariadb-libs<br/>

## 3.2 初始化数据库
创建数据库<br/>
mysql -uroot -hlocalhost -p'123456' < mariadb/db1.sql<br/>
导入测试数据<br/>
mysql -uroot -hlocalhost -p'123456' < mariadb/db2.sql<br/>
设置root密码<br/>
select * from mysql.user where user='root';<br/>
delete from mysql.user where user='root' and host not like 'localhost';<br/>
update mysql.user set password=PASSWORD('123456'),host='%' where user='root' and host='localhost';<br/>
flush privileges;<br/>

## 3.3 增删查改SQL
连接数据库<br/>
mysql -hlocalhost -uroot -p123456 ge<br/>
其他<br/>
SHOW TABLE STATUS LIKE "%data_aging%";<br/>
SHOW CREATE DATABASE ge;<br/>
SHOW CREATE TABLE tb_data_aging;<br/>
