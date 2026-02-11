## 下载centos.iso 

https://wiki.centos.org/Download


## 分区

* legacy模式
  * /boot 分区：
  * / 分区：ext4，剩余所有容量

* uefi模式
  * /boot/efi 分区：EFI 格式，200M大小
  * /boot 分区：ext4格式，1G大小
  * / 分区：etx4格式，剩余所有容量

## 修改网卡名

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


## 修改网卡配置文件

查看网卡配置文件,在目录 /etc/sysconfig/network-scripts/
~~~conf
TYPE="Ethernet"                 网络类型以太网,默认就行
BOOTPROTO="static"              ip获取方式(dhcp或static)
DEFROUTE="yes"                  默认网卡
IPV4_FAILURE_FATAL="no" 
NAME="enp3s0"                   网卡名字
UUID="36f15ef3-cb3a-47f5-a402-37488dec5ab6"
DEVICE="enp3s0"                 物理网卡名字
ONBOOT="yes"                    随boot启动而启动
IPADDR="192.168.1.11"           ip地址
PREFIX="24"                     子网掩码(和NETMASK 2选1)
NETMASK="255.255.255.0"         子网掩码(和PREFIX 2选1)
GATEWAY="192.168.1.1"           网关
DNS1="202.101.172.35"           DNS

IPV6INIT="no"                   禁用ipv6
~~~

## 禁用IPV6

```
echo "net.ipv6.conf.all.disable_ipv6 = 1"     >> /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.lo.disable_ipv6 = 1"      >> /etc/sysctl.conf

sysctl -p
```




## 重启网络配置
systemctl restart network

## DNS配置文件
如果还是上不了网,或者路由器没有配置DNS,手动设置一下/etc/resolve.conf
~~~
nameserver 202.101.172.35
~~~

## 关闭firewalld 和 selinux
```sh
#关闭firewall 并 取消开机自启
systemctl disable firewalld --now
#修改selinux配置文件
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config 
```




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




## 修改时区

```sh
rm -f /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```


## 修改yum软件源

默认的可能已经不能用了，注释mirrorlist，修改baseurl为下面这个
```
baseurl=http://vault.centos.org/7.9.2009/os/$basearch/
```

使用sed命令完成
```sh
sed -i '/mirrorlist/s/^/#/' /etc/yum.repos.d/CentOS-Base.repo

sed -i '/#baseurl/a baseurl=http://vault.centos.org/7.9.2009/os/$basearch/' /etc/yum.repos.d/CentOS-Base.repo
```

## 安装常用软件
```
yum install -y epel-release net-tools lrzsz telnet wget vim perl gcc kernel-devel htop traceroute yum-utils lvm2

net-tools       网络相关命令
lrzsz           shell工具上传下载命令
epel-release    红帽系列额外软件包
vim             替代vi的编辑器
```

## 主机名

~~~
hostnamectl set-hostname xxx
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