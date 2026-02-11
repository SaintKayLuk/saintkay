# ubuntu 通过 APT 安装

把 dep 包上传到服务器上

```sh
dpkg -i mysql-apt-config_0.8.36-1_all.deb

apt update
# 跳出选择框就选择 8.4 LTS 就行

# 安装mysql
apt install mysql-server

# 安装过程中设置 root 密码
```

安装的数据库版本是在 install 之前就确定的，如果需要更改，则重新配置

```sh
dpkg-reconfigure mysql-apt-config
apt update
```

