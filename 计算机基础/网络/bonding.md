# Bond

多个网卡(网线)使用同一个ip，实现网卡或者网线冗余

多个模式

* balance-rr (Mode 0) - 轮询策略
  * 必须要求交换机端也配置对应的链路聚合（通常是动态或静态聚合）
* active-backup (Mode 1) - 主备策略（最常用/最安全）
  * 只有一块网卡活跃
  * 不需要交换机做任何特殊配置
* balance-xor (Mode 2) - 异或策略
* broadcast (Mode 3) - 广播策略
* 802.3ad (Mode 4) - LACP 动态链路聚合（高性能首选
* balance-tlb (Mode 5) - 自适应传输负载均衡
* balance-alb (Mode 6) - 自适应负载均衡


| 模式名称 | 代号 | 核心逻辑 | 交换机配置 | 推荐指数 | 典型用途 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| active-backup | Mode 1 | 一主一备，断了才切换 | 不需要 | ⭐⭐⭐⭐⭐ | 通用首选，稳定省心 |
| 802.3ad | Mode 4 | 动态聚合，带宽叠加 | 必须配 LACP | ⭐⭐⭐⭐ | 高性能服务器 (需交换机支持) |
| balance-rr | Mode 0 | 轮询，依次发送 | 需配聚合 | ⭐⭐ | 旧式高吞吐 (易乱序，慎用) |
| broadcast | Mode 3 | 广播，所有口同时发 | 不需要 | ⭐ | 极特殊高可靠/心跳/调试 |
| balance-xor | Mode 2 | 哈希，按地址固定路径 | 需配静态聚合 | ⭐⭐ | 特定负载平衡需求 |
| balance-tlb/alb | Mode 5/6 | 自适应，智能调节 | 不需要 | ⭐⭐ | 特殊无交换机负载均衡 |





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


进 /etc/netplan 目录下

有 00-installer-config.yaml 则修改，没有则新建，内容如下


配置 mode4
```yaml
network:
  version: 2
  ethernets:
  # LACP 模式下，物理网卡不需要 IP，也不需要开启 STP 等，保持最简
    eno1: {}
    eno2: {}
  bonds:
    bond4:
      interfaces:
        - eno1
        - eno2

      # IP 地址配置在 bond0 接口上，而不是物理网卡上
      addresses:
        - 192.168.1.100/24   # 替换为你的静态 IP
      parameters:
        # 核心：设置为 802.3ad (LACP)
        mode: 802.3ad
        
        # LACP 数据包发送频率：fast (1秒) 或 slow (30秒)
        # 建议设为 fast 以便更快检测链路故障
        lacp-rate: fast
        
        # 选择策略：通常使用 layer3+4 (基于源/目IP + 端口哈希)，负载均衡效果最好
        transmit-hash-policy: layer3+4
        
        # MII 监控间隔 (毫秒)
        mii-monitor-interval: 100
        
        # 802.3ad 特定的超时时间 (可选，通常默认即可)
        # ad-select: stable (默认) 或 bandwidth, count
        
      routes:
        - to: default
          via: 192.168.1.1   # 替换为你的网关
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1

```


## windows server 设置 bonding


服务器管理页面，创建 NIC Team
1. 点击右上角 “任务” → “新建组”
2. 组名称：例如 Team1，或者bond1 这种等
3. 勾选要绑定的 两个或多个物理网卡（如 Ethernet0 + Ethernet1）
4. 成组模式：交换机独立（此方式最简单，不需要配置交换机）
5. 负载平衡模式：动态

