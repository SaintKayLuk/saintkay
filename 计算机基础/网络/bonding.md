多个网卡(网线)使用同一个ip，实现网卡或者网线冗余


mode4 ↓
BONDING_OPTS="mode=4 miimon=100 lacp_rate=1"

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

BONDING_OPTS="mode=1 miimon=100"    #指定bonding模式 
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


