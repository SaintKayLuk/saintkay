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




# 安装 6.0 版本

从这个地址 查看安装脚本 [download](https://www.zabbix.com/download)


例：ubuntu 22.04 安装 zabbix 6.0

安装 zabbix-server frontend agent2
```sh
wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_6.0+ubuntu22.04_all.deb
dpkg -i zabbix-release_latest_6.0+ubuntu22.04_all.deb
apt update
apt install zabbix-server-mysql zabbix-frontend-php zabbix-nginx-conf zabbix-sql-scripts zabbix-agent2

# 可选，安装 agent2 plugins
apt install zabbix-agent2-plugin-mongodb zabbix-agent2-plugin-mssql zabbix-agent2-plugin-postgresql
```


手动安装数据库，例如 [安装 mysql](../../数据库/mysql/安装mysql.md)

```sh
mysql -uroot -p

mysql> create database zabbix character set utf8mb4 collate utf8mb4_bin;
mysql> create user zabbix@localhost identified by 'password';
mysql> grant all privileges on zabbix.* to zabbix@localhost;
mysql> set global log_bin_trust_function_creators = 1;
mysql> quit;
```

导入 mysql 基础数据
```sh
zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p zabbix
```

禁用 log_bin_trust_function_creators 选项 
```sh
mysql -uroot -p

mysql> set global log_bin_trust_function_creators = 0;
mysql> quit;
```

修改 zabbix 配置文件 /etc/zabbix/zabbix_server.conf
```conf
DBPassword=password
```

启动并加入开启自启
```sh
systemctl enable zabbix-server zabbix-agent2 nginx php8.1-fpm --now
```


**注意：如果用 ip 并且用 80 端口访问，则需要注释一行默认配置，或者修改 zabbix 的端口**

配置文件 /etc/nginx/nginx.conf 注释如下一行，否则 80 端口会跳转默认页面
```conf
#include /etc/nginx/sites-enabled/*
```


## 配置 zabbix

配置页面语言，如果没有中文可选，则需要在服务器本地配置

```sh
# 安装中文语言包（如果未安装）
sudo apt install language-pack-zh-hans

# 生成中文 locale
sudo locale-gen zh_CN.UTF-8

# 重启php
sudo systemctl restart php8.1-fpm
```

# 安装 6.0 版本 agent



## windows 版本 安装包

[Zabbix agent 下载](https://www.zabbix.com/download_agents?version=6.0+LTS&release=6.0.43&os=Windows&os_version=Server+2016+%2B&hardware=amd64&encryption=OpenSSL&packaging=MSI&show_legacy=0)

一直下一步，最后填一个 Zabbix server 的地址就行

## windows 版本 压缩包安装

解压之后，放一个目录下，提前修改配置文件，指定server的地址

并安装成服务
```batch
cd C:\Program Files\zabbix_agent\bin
zabbix_agentd.exe --config ../conf/zabbix_agentd.conf --install
net start "Zabbix Agent"
```



