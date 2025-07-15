## 下载 ubuntu 22.04 LTS

https://ubuntu.com/download/server

## 安装过程


1. 选择语言：默认选择 English 就行
2. 更新安装程序(可选)：如果跳出这一选择，可以选择更新
3. 选择键盘布局：默认就行
4. 选择安装类型，选第一个 **Ubuntu Server** 就行
    ```
    choose the type of installation

    (x) Ubuntu Server
    ()  Ubuntu Server (minimized)
    ()  Search for third-party drivers
    ```
5. 配置网络
    ```sh
    Network configuration

    #配置ipv4和ipv6，Automatic(DHCP)、Manual、Disabled
    eth -         

    #创建bond，如果只有一根网线则没有必要
    Create bond
    ```

    手动设置网络
    ```
    subnet:         网段，例如xx.xx.xx.xx/xx
    address:        IP地址，xx.xx.xx.xx
    gateway:        网关
    name servers:   dns地址，例如杭州电信 202.101.172.35
    Search domains: 搜索域访,访问一个“不完整的主机名”时，会自动加上这个域名后缀去尝试解析。例如设置了 xxx.com，则访问 web1，相当于访问 web1.xxx.com
    ```
6. 设置代理：默认不添加，直接选 Done
7. Ubuntu archive mirror configuration：等待加载完，点 Done ，如果testing失败了呢，默认镜像源需要改？
8. 是否更新安装程序，如果有的话，我们选择 **Update to the new installer**
    ```
    Installer update available
    ...
    ```
9.  磁盘分区
    1. 第一块硬盘做系统盘，1G给/boot ，剩下的给/ 
    2. 第二块硬盘用lvm方式，挂载 /data 等，用作数据盘
    
            如果使用的是台式机来装ubuntu系统，出现硬盘识别不到的情况，则进bios，关闭 Intel RST
            如果原来的分区删不掉，则通过 Ctrl + Alt + F2 进入终端
                fdisk /dev/sdX 
                然后在 fdisk 命令行输入：
                  p （查看分区）
                  d （删除分区，重复多次直到所有分区都删掉）
                  w （保存更改并退出）
                删除所有分区后w保存退出，再 Ctrl + Alt + F1 回安装界面




10. 设置用户名密码等，
    ```sh
    Your name                 #名字，可以写成服务器名字或者自己的名字
    Your server name          #服务器名字，就是 hostname
    Pick a username           #用于登录的普通用户的用户名，此用户默认拥有sudu权限
    Choose a password         #输入密码
    Confirm your password     #确认密码
    ```
11. 升级到Ubuntu Pro，企业付费服务，没有必要，我们选skip，选 **Continue**
    ```
    Upgrade to Ubuntu Pro

    
    ()  Enable Ubuntu Pro
    (x) Skip Ubuntu Pro setup for now
    ```
12. 安装openssh服务，可以安装，不然没有ssh，无法远程登录
    ```
    SSH configuration

    [X] Install OpenSSH server
    ```
13. 可选的安装软件，可以按需勾选
    ```
    Featured server snaps
    ...
    ```
14. 等待 Installation complete，然后点 Reboot Now





## 设置root用户登陆(安装过程中不能设置root密码)

1. 用安装过程中设置的username和password登陆后设置root密码
```
sudo passwd root
```

2. 设置root用户可以通过ssh登陆
```sh
# 切换root用户
su root

# 编辑ssh配置文件，设置 -> PermitRootLogin yes
vi /etc/ssh/sshd_config

systemctl restart sshd
```

3. 删除安装过程中的用户(可选)

## 更换镜像源

先备份一下

```sh
cp  /etc/apt/sources.list  /etc/apt/sources.list.bak
```

替换镜像源，镜像源列表

* 163镜像：http://mirrors.163.com/ubuntu/
* 清华源镜像：https://mirrors.tuna.tsinghua.edu.cn/ubuntu/
* 中科大镜像：https://mirrors.ustc.edu.cn/ubuntu/
* 阿里云镜像：http://mirrors.aliyun.com/ubuntu/

替换的旧字符串不一定是 **http://cn.archive.ubuntu.com/ubuntu/**
```sh
# 替换的旧字符串
sed -i 's/http:\/\/cn.archive.ubuntu.com\/ubuntu\//https:\/\/mirrors.aliyun.com\/ubuntu\//g' /etc/apt/sources.list
```

更新软件包索引
```sh
apt update
```

升级软件包到最新版本
```sh
apt upgrade
```

## 配置ip

networkd 和 NetworkManager

* networkd：较轻量的网络管理工具，专注于系统服务和基础网络配置
* NetworkManager：

网络配置 用 netplan 来配置
```sh
vi /etc/netplan/00-installer-config.yaml

network:
  ethernets:
    ens160:                     #网卡名
      addresses:
      - 192.168.2.12/24
      nameservers:              #dns
        addresses:
        - 192.168.2.1
      routes:
      - to: default
        via: 192.168.2.1        #网关，也就是默认路由
  version: 2
#  renderer: NetworkManager     #默认使用networkd，所以此项不需要设置
```


## 禁用 ipv6

```
echo "net.ipv6.conf.all.disable_ipv6 = 1"     >> /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.lo.disable_ipv6 = 1"      >> /etc/sysctl.conf

sysctl -p
```

## 禁用swap

```
vi /etc/fstab

注释或者删除 swap 那行

swapoff -a
```

## 修改 .bashrc

修改 .bashrc 文件

```sh
alias ll='ls -alF'
# 改为↓ 习惯问题
alias ll='ls -lF'
```
## 设置时区 (可选)

查看当前时间和时区
```sh
timedatectl
```

设置为亚洲上海时间
```sh
timedatectl set-timezone Asia/Shanghai
```

设置之后，可能需要重启，不重启 crontab 的时间可能不对，目前还没找到原因，重启后正常


