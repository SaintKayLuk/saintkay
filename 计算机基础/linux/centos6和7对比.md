
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


# 服务管理

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



# 网络设置

| 差异               | centos 6.x            | centos 7.x                                    |
|------------------|-----------------------|-----------------------------------------------|
| 网卡名             | eth0                  | ens33等(根据网卡型号等算出)                   |
| 网络配置命令       | ifconfig              | ip                                            |
| 网络配置图形化命令 | setup                 | nmtui                                         |
| 网络服务           | 默认使用 network 服务 | 默认使用 NetworkManager 服务(network作为备用) |


配置文件目录
```
/etc/sysconfig/network-scripts/网卡名
```

配置内容
```
TYPE="Ethernet"                 网络类型以太网,默认就行
BOOTPROTO="static"              ip获取方式(dhcp或static)
DEFROUTE="yes"                  默认网卡
NAME="enp3s0"                   网卡名字
DEVICE="enp3s0"                 物理网卡名字
ONBOOT="yes"                    随boot启动而启动
IPADDR="192.168.1.11"           ip地址
PREFIX="24"                     子网掩码(centos 6.x 使用NETMASK="255.255.255.0")
GATEWAY="192.168.1.1"           网关
DNS1="202.101.172.35"           DNS
```

物理网卡名称 DEVICE 和网卡名称 NAME 必须一致
DNS必须为 DNS1 DNS2等


## centos 7.x 修改网卡名

1. 修改网卡配置文件名(最好将原来的文件备份)
```sh
mv /etc/sysconfig/network-scripts/ifcfg-ens33 /etc/sysconfig/network-scripts/ifcfg-eth0
```
2. 修改网卡配置文件内容
```
vi /etc/sysconfig/network-scripts/ifcfg-eth0
NAME=eth0
DEVICE=eth0
```
3. 修改grup配置文件,在 GRUB_CMDLINE_LINUX 后面添加 <font color="red">net.ifnames=0 biosdevname=0</font>
```
vi /etc/default/grub
GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=cl/root rd.lvm.lv=cl/swap nomodeset rhgb quiet net.ifnames=0 biosdevname=0"
```
4. 更新grup配置文件，加载新的参数
```
grub2-mkconfig -o /boot/grub2/grub.cfg
```
5. 重启，重新读取网卡
```
shutdown -r
```




