## firewalld 和 iptables 区别

firwalld 可以动态加载规则，而iptables需要重新启动加载一遍规则
意味着，iptables重启会有短暂的关闭时间，而firwalld在reload过程中，会保持现有连接，不会导致流量中断
```sh
#iptables修改规则后，使其生效
systemctl restart iptables
#firewalld修改规则后，重新加载使其生效
firewall-cmd --reload
```

## 配置


### 配置文件


系统配置文件
```sh
#主配置文件
/etc/firewalld/firewalld.conf
#配置目录
/etc/firewalld/
```


软件默认配置，例如zone，serice等，这个是默认配置目录，不应更改，如果需要更改，复制到/etc/firewalld/下相应的位置
```
/usr/lib/firewalld/
```


### 临时配置和永久配置

添加和修改规则的时候不添加 --permanent ，则是临时修改
当然，有些命令是不不区分临时和永久的，例如修改默认区域，则会直接修改配置文件

例：将当前运行配置写入到永久配置
```sh
firewall-cmd --runtime-to-permanent
```
例：修改默认域为trusted，此命令执行完之后，会直接修改配置文件 firewalld.conf
```sh
firewall-cmd --set-default-zone=trusted
```

永久配置的规则，会保存在 /etc/firewalld/zones 下对应的域文件中，例如 public.xml，当然我们也可以直接修改这个文件，并且 reload 一下

### 配置文件firewalld.conf
```conf
# 默认域，为空也是public
DefaultZone=public

# Minimal mark
# Marks up to this minimum are free for use for example in the direct 
# interface. If more free marks are needed, increase the minimum
# Default: 100
MinimalMark=100

# 退出或者停止firwalld的时候是否清空防火墙规则，默认yes
CleanupOnExit=yes

# Lockdown
# If set to enabled, firewall changes with the D-Bus interface will be limited
# to applications that are listed in the lockdown whitelist.
# The lockdown whitelist file is lockdown-whitelist.xml
# Default: no
Lockdown=no

# 对IPv6数据包执行反向路径筛选器测试。如果对数据包的回复将通过数据包到达的同一接口发送，则数据包将匹配并被接受，否则将被丢弃。IPv4的rp_filter使用sysctl进行控制，默认yes
IPv6_rpfilter=yes

# IndividualCalls
# Do not use combined -restore calls, but individual calls. This increases the
# time that is needed to apply changes and to start the daemon, but is good for
# debugging.
# Default: no
IndividualCalls=no

# LogDenied
# Add logging rules right before reject and drop rules in the INPUT, FORWARD
# and OUTPUT chains for the default rules and also final reject and drop rules
# in zones. Possible values are: all, unicast, broadcast, multicast and off.
# Default: off
LogDenied=off

# 为了安全使用iptables和连接跟踪帮助程序，建议关闭AutomaticHelpers，配置会更改/proc/sys/net/netfilter/nf_conntrack_helper 的值
# 设置 yes、no、system，默认system
AutomaticHelpers=system

# 是否允许数据包进入多个区域，默认允许，我们一般情况下关闭它，设置no
AllowZoneDrifting=yes
```


## firewalld命令

firewalld的服务名为 firewalld，命令为firewall-xxx

如果没有 firewall-config 命令，则安装一下
```sh
yum install -y firewall-config
```

* **firewall-cmd**
  * 防火墙命令
  * 防火墙没有开启的时候使用不了
* **firewall-config**
  * 防火墙图形化界面，当时，需要先有图形化界面，没有安装图形化界面还是用不了
* **firewall-offline-cmd**
  * 防火墙离线命令
  * 防火墙关闭的时候也能使用
  * 命令和 firwall-cmd 基本类似


### firewall-cmd
```
firewall-cmd [OPTIONS...]
    --version               查看版本
    --state                 查看防火墙状态
    --reload                重新加载 firewalld，修改了规则后，需要 reload 使其生效
    --permanent             永久生效，添加此参数，会将配置写入配置文件，在重启后仍旧生效
    --list-all              查看当前域的所有配置信息

    --get-zones                             查看所有域
    --get-active-zones                      查看绑定的网卡的活跃区域
    --get-default-zone                      查看默认区域
    --get-zone-of-interface=em1             查看某个网卡的域
    --zone=public --change-interface=eth0   设置某个网卡为某个域

    --get-services              查看所有服务
    --list-services             查看放行的所有服务
    --add-service=<service>     当前域添加某个服务，可以指定域 --zone=<zone>
    --remove-service=<service>  当前域删除某个服务

    --add-source=<ip,ip...>     在域中添加ip或者网段，根据域的规则来决定这些ip的访问规则

    --list-ports                        查看当前域的所有开放端口
    --add-port={ports}/protocol         开放某个，或者多个端口
    --remove-port={ports}/protocol      删除一个或多个端口

    --add-masquerade            地址伪装，用于转发其他地址
    --add-forward-port=port=<转发端口>:proto=<协议>:toport=<被转发的端口>
    --add-forward-port=port=<转发端口>:proto=<协议>:toport=<被转发的端口>:toaddr=<被转发的ip地址>
```

例：开放8080的tcp端口
```sh
firewall-cmd --add-port=8080/tcp
```
例：开放222和333的 udp 端口
```sh
firewall-cmd --add-port={222,333}/udp
```


转发接口还需要开启路由转发，和地址伪装
例：端口映射和路由转发
```sh
#前置条件
echo "1" > /proc/sys/net/ipv4/ip_forward
firewall-cmd --add-masquerade

#转发本机 8080 端口到 80 端口
firewall-cmd --permanent --add-forward-port=port=8080:proto=tcp:toport=80 

#转发本机 7112 端口到 172.16.1.150 的 7112 端口
firewall-cmd --permanent --add-forward-port=port=7112:proto=tcp:toport=7112:toaddr=172.16.1.250
```


## 区域

firewalld的区域有一下原则
1. 流量只进入一个区域
2. 流量只能从一个区域流出
3. 一个区域定义一个信任级别
4. 区内（同一区内）默认为允许
5. 区间（区与区之间）默认为拒绝

原则4和原则5是 原则3的结果
原则 4 可通过区域选项 --remove-forward 进行配置
原则 5 可通过添加新策略进行配置。


---


不同区域有不同策略，默认public区域，可以通过命令查看

一个网卡只能绑定一个区域，

下面是一些预定义域，从不可信到可信排序
* drop 所有传入的网络包都会被丢弃，没有回复，只能传出网络
* block 所有传入的网络都会被拒绝，能传出网络
* public 仅接受选定的传入的连接
* external
* dmz
* work
* home
* internal
* trusted 接受所有网络连接

## 服务

firewalld可以直接配置服务，来设置流量的进出，因为服务已经配置好了端口等，
默认有一些服务，在 /usr/lib/firewalld/services/ 下，当然自己也可以在 /etc/firewalld/services/ 下添加 
