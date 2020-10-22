
# chentos 6.x 和 centos 7.x 区别
| 差异       | centos 6.x             | centos 7.x                                               |
|----------|------------------------|----------------------------------------------------------|
| 内核版本   | 2.6.x                  | 3.10.x                                                   |
| 文件系统   | ext4                   | xfs                                                      |
| 防火墙     | iptables               | firewalld                                                |
| 默认数据库 | Mysql                  | MariaDB                                                  |
| 时间同步   | ntpg -p                | chronyc sources                                          |
| 修改时区   | /etc/sysconfig/clock   | timedatectl set-timezone Asia/Shanghai                   |
| 修改语言   | /etc/sysconfig/i18n    | localectl set-locale LANG=zh_CN.UTF-8                    |
| 主机名     | /etc/sysconfig/network | /etc/hostname    <br/>  hostnamectl set-hostname xxx.com |


# 服务管理区别

| 操作行为               | centos 6.x             | centos 7.x                |
|--------------------|------------------------|---------------------------|
| 启动指定服务           | service 服务名 start   | systemctl start 服务名    |
| 关闭指定服务           | service 服务名 stop    | systemctl stop 服务名     |
| 重启指定服务           | service 服务名 restart | systemctl restart 服务名  |
| 查看指定服务状态       | service 服务名 status  | systemctl status 服务名   |
| 查看所有服务状态       | service --status-all   | systemctl list-units      |
| 设置服务自启动         | chkconfig 服务名 on    | systemctl enable 服务名   |
| 取消服务自启动         | chkconfig 服务名 off   | systemctl disable 服务名  |
| 查看所有服务自启动状态 | chkconfig --list       | systemctl list-unit-files |



# 网络服务区别











