多个网卡(网线)使用同一个ip，实现网卡或者网线冗余

1. 新建一个bond0文件
```sh
vi /etc/sysconfig/network-scripts/ifcfg-bond0

TYPE=Bond               
DEVICE=bond0
NAME=bond0
BOOTPROTO=none          
ONBOOT=yes
IPADDR=10.101.230.30            #ip
PREFIX=27                       #子网掩码
GATEWAY=10.101.230.1            #网关
DNS1=8.8.8.8                    #DNS1
DNS2=114.114.114.114            #DNS2
BONDING_MASTER=yes              #
BONDING_OPTS="mode=1 miimon=100"#  指定bonding模式 
```

2. 修改需要bonding的网卡内容，例如ifcfg-eno1和ifcfg-eno2
```sh
vi /etc/sysconfig/network-scripts/ifcfg-eno1


TYPE=Ethernet
BOOTPROTO=none      #改成none或者static
ONBOOT=yes
...
#IPADDR=X.X.X.X     #注释ip设置
#PREFIX=
#GATEWAY=
...
#新增以下两项
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