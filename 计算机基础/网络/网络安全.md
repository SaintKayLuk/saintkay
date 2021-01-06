

## TCP Wrappers

对有状态连接(TCP)的特定服务进行安全检测并实现访问控制，界定方式是凡是调用libwarp.so库文件的程序就可以受TCP_Wrapper的安全控制

判断方式
1. 查看对应服务命令所在的位置，例如 sshd 服务
```
[root@localhost ~]# which sshd
/usr/sbin/sshd
```
2. 查看指定命令执行时是否调用 libwrap.so 文件
```
[root@localhost ~]# ldd /usr/sbin/sshd |grep libwrap.so
        libwrap.so.0 => /lib64/libwrap.so.0 (0x00007fae987f9000)
```

### 配置文件

```
/etc/hosts.allow
/etc/hosts.deny
```

/etc/hosts.allow 优先级大于 /etc/hosts.deny ,默认两个文件都为空，没有限制。
当有客户端请求时，判断ip是否存在于 /etc/hosts.allow 则放行，如果ip不存在于 /etc/hosts.allow ,继续判断该ip是否存在于 /etc/hosts.deny ，如果存在则禁止连接，如果不存在，则放行

#### 配置文件语法

```
service_list@host:client_list
```

* service_list  服务列表，可以是多个，用 , 隔开，例如 sshd,rpcd
* @host         设置允许或禁止从哪个网卡进入(多网卡)，如果不写，则代表所有
* client_list   访问者地址，如果有多个，可以使用 空格 或者 , 隔开
  * 基于ip地址的写法 192.168.1.11 192.168.2.22
  * 基于主机名的写法 www.saintkay.com www.saintcat.cn
  * 基于网段的写法 192.168.1.1/24 192.168.2.1/24
  * 内置ACL的写法 all(所有主机) local(本地主机)

例：不允许 192.168.1.123 的ip访问 ssh 服务
```
/etc/hosts.allow    空着

/etc/hosts.deny的内容
[root@localhost ~]# cat /etc/hosts.deny
sshd:192.168.1.123
```



