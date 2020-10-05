## 下载centos.iso 

https://wiki.centos.org/Download




## 修改网卡配置文件


查看网卡配置文件,在目录 /etc/sysconfig/network-scripts/
~~~
TYPE="Ethernet"                 网络类型以太网,默认就行
BOOTPROTO="static"              ip获取方式(dhcp或static)
DEFROUTE="yes"                  默认网卡
IPV4_FAILURE_FATAL="no" 
NAME="enp3s0"                   网卡名字
UUID="36f15ef3-cb3a-47f5-a402-37488dec5ab6"
DEVICE="enp3s0"                 物理网卡名字
ONBOOT="yes"                    随boot启动而启动
IPADDR="192.168.1.11"           ip地址
PREFIX="24"                 
GATEWAY="192.168.1.1"           网关
NETMASK="255.255.255.0"         子网掩码
DNS1="202.101.172.35"           DNS
~~~

systemctl restart network

## DNS配置文件
如果还是上不了网,或者路由器没有配置DNS,手动设置一下/etc/resolve.conf
~~~
nameserver 202.101.172.35
~~~

## 防火墙
~~~
查看firewall是否开启
$ firewall-cmd --state
running

关闭firewall
$ systemctl stop firewalld

取消开机自启
$ systemctl disable firewalld
~~~




## swap
~~~
[root@13 ~]# free -h
              total        used        free      shared  buff/cache   available
Mem:            15G        261M         14G        8.9M        446M         14G
Swap:          7.8G          0B        7.8G
~~~
临时关闭，重启失效
~~~
[root@13 ~]# swapoff -a
~~~
永久关闭
~~~
vi /etc/fstab
注释掉swap那一行
~~~

重启生效

~~~
[root@13 ~]# free -h
              total        used        free      shared  buff/cache   available
Mem:            15G        257M         14G        8.9M        405M         14G
Swap:            0B          0B          0B
~~~

## selinux
~~~
查看是否开启
[root@13 ~]# sestatus
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          disabled
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Max kernel policy version:      28


修改 /etc/selinux/config文件

vi /etc/selinux/config
将SELINUX 设为disabled
SELINUX=disabled

立即重启 shutdown -r now

[root@13 ~]# sestatus
SELinux status:                 disabled
~~~


## 主机名

~~~
立即生效，重启失效，重启获取 /etc/hostname得值
$ hostname "你取得主机名"

重启生效
$ echo "你取的主机名" > /etc/hostname
~~~


## 删除恢复

安装extundelete


## 操作配置

### 导入数字证书
~~~
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
~~~
### 配置文件
根据自己习惯修改
~~~
vi ~/.bashrc

添加
alias vi='vim'
...
~~~
### vim配置
没有此文件新建一个
~~~
~/.vimrc
~~~

添加新用户配置

~~~
vi /etc/default/useradd

INACTIVE=0      密码过期后宽限天数，默认-1，永不过期
~~~