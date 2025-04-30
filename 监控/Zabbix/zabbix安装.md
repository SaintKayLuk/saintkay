

# 安装 5.0 版本


1. 安装 server 和 anent
```sh
#添加yum源
rpm -ivh https://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-release-5.0-1.el7.noarch.rpm
#安装 server 和 agent
yum install -y zabbix-server-mysql-5.0.28 zabbix-agent-5.0.28
```


2. 安装zabbix web端，需要启用zabbix-frontend 库 和添加 redhat 三方源
```sh
#启用 zabbix-frontend 
#也可以手动修改 zabbix.repo 文件，修改enabled=1
yum-config-manager --enable zabbix-frontend

#添加 redhat scl源
yum install -y centos-release-scl
```


3. 安装 web端
```sh
#安装
yum install -y zabbix-web-mysql-scl-5.0.28 zabbix-nginx-conf-scl-5.0.28
```


4. 初始化数据库，可以本地mysql，也可以远程mysql

```sh
#创建库
mysql> create database zabbix character set utf8 collate utf8_bin;

#创建zabbix用户 (zabbix@%)
mysql> create user zabbix identified by 'password';
#本地mysql，只允许localhost访问，zabbix@localhost
mysql> create user zabbix@localhost identified by 'password';

#赋予zabbix库的权限
mysql> grant all privileges on zabbix.* to zabbix;

#初始化数据
zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz | mysql -uzabbix -pzabbix -Dzabbix
```

5. 配置前端 php 和 nginx

**修改nginx配置文件**
```
vi /etc/opt/rh/rh-nginx116/nginx/conf.d/zabbix.conf

取消注释
# listen 80;
# server_name example.com;

vi /etc/opt/rh/rh-nginx116/nginx/nginx.conf
注释掉默认的80端口的主页
```

**修改php配置文件**
```sh
vi /etc/opt/rh/rh-php72/php-fpm.d/zabbix.conf 

listen.acl_users = apache
    改为
listen.acl_users = apache,nginx

#修改默认时区，并取消注释
; php_value[date.timezone] = Europe/Riga
    改为
php_value[date.timezone] = Asia/Shanghai
```

**修改中文乱码问题**

```sh
#windows电脑中找个字体 在 C:\Windows\Fonts 新宋体

#上传 字体文件到此目录
/usr/share/zabbix/assets/fonts
#修改字体后缀
mv simsun.ttc simsun.ttf

#修改配置文件
/usr/share/zabbix/include/defines.inc.php

define('ZBX_GRAPH_FONT_NAME',           'graphfont');
    改为
define('ZBX_GRAPH_FONT_NAME',           'simsun');
```

6. 启动zabbix

```sh
systemctl restart zabbix-server zabbix-agent rh-nginx116-nginx rh-php72-php-fpm
```


