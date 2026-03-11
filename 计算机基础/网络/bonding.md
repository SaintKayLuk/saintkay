多个网卡(网线)使用同一个ip，实现网卡或者网线冗余


mode4 ↓
BONDING_OPTS="mode=4 miimon=100 lacp_rate=1"



## centos 7 设置 bonding
1. 新建一个bond0文件
```sh
touch /etc/sysconfig/network-scripts/ifcfg-bond0
```

内容如下
```conf
TYPE=Bond
BOOTPROTO=none  
NAME=bond0          
DEVICE=bond0
ONBOOT=yes

IPADDR=10.101.230.30                #ip
PREFIX=27                           #子网掩码
GATEWAY=10.101.230.1                #网关
DNS1=8.8.8.8                        #DNS1
DNS2=114.114.114.114                #DNS2

BONDING_OPTS="mode=1 miimon=100"    #指定bonding模式，参数等
```

2. 修改需要bonding的网卡内容，例如ifcfg-eno1和ifcfg-eno2
```sh
vi /etc/sysconfig/network-scripts/ifcfg-eno1
```

网卡 eno1 内容
```conf
BOOTPROTO=none
DEVICE=eno1
ONBOOT=yes

MASTER=bond0
SLAVE=yes
```
网卡 eno2 内容
```conf
BOOTPROTO=none
DEVICE=eno2
ONBOOT=yes

MASTER=bond0
SLAVE=yes
```


3. 重启网络服务器
```sh
systemctl restart network
```


查看bonding状态
```sh
cat /proc/net/bonding/bond0
```


## ubuntu 22.04 设置 bonding



## windows server 设置 bonding


服务器管理页面，创建 NIC Team
1. 点击右上角 “任务” → “新建组”
2. 组名称：例如 Team1，或者bond1 这种等
3. 勾选要绑定的 两个或多个物理网卡（如 Ethernet0 + Ethernet1）
4. 成组模式：交换机独立（此方式最简单，不需要配置交换机）
5. 负载平衡模式：动态

