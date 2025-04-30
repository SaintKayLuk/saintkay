## DNS 协议

* 正向解析：域名 --> IP
* 反向解析：IP --> 域名 

域名和ip地址的对应
www.google.com.
以 **.** 区分
* .       是根域
* com     是顶级域
* google  是二级域名
* www     是三级域名

最多可以分支 127 层，每层最多由 63 个字符组成，中间用点（.）分隔。域名总长度不能超过 255 个字符，不区分大小写。可以是字母，数字，-，但是 - 不能为首

**.** 为dns根，在 DNS 级别上，www.google.com 不能算是严格意义上的 FQDN，因为它漏写了最后的一个点 **.** www.google.com.



## 配置文件

### DNS解析配置文件
* 局部：即网卡配置文件，里面只能写某个网卡的dns
```
/etc/sysconfig/network-scripts/ifcfg-eth0

DNS1=ip
DNS2=IP
```

* 全局：所有网卡的dns
```
/etc/resolv.conf

nameserver ip
```

* 相关配置文件：手动指定域名和ip
```
/etc/hosts
```

* 优先级
```
/etc/hosts > /etc/resolv.conf > /etc/sysconfig/network-scripts/ifcfg-eth0
```

### DNS服务配置文件

* /etc/named.conf
  主配置文件
* /etc/named.rfc1912.zones
  区域配置文件
* /var/named/目录下
  数据配置文件





## 安装DNS服务器


* 软件名为bind
* 服务名为named
* 端口
  * UDP 53：用于数据通信，即域名解析
  * TCP 53：用户数据同步，即DNS主从服务器之间同步



### 安装
以centos为例
~~~
yum install -y bind
~~~

修改named.conf, 设为any
listen-on port 53 { any; }; 
allow-query     { any; }; 

~~~
$ vi /etc/named.conf

options {

        listen-on port 53 { any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        recursing-file  "/var/named/data/named.recursing";
        secroots-file   "/var/named/data/named.secroots";
        allow-query     { any; };

...

include "/etc/named.rfc1912.zones"; 
include "/etc/named.root.key"; 
~~~

修改 named.rfc1912.zones 配置文件

~~~
新添加一个解析, 根域为saintkay.com, 文件名为saintkay.com.zone
zone "saintkay.com" IN {

        type master;
        file "saintkay.com.zone";
        allow-update { none; };
        allow-transfer { none; };

}; 
~~~

* type 后面跟的是 master 或 slave, 配置dns服务器主从，不配置主从，则用master
* file 解析文件名，根据/etc/named.conf文件中的 **directory       "/var/named"; ** 决定解析文件位置，所以文件路径为 **/var/named/saintkay.com.zone**
* allow-update "允许更新"，允许从服务器更新，填写从服务器ip
* allow-transfer “允许传输”，就是指可以接收你的更新的服务器。当然，该指令仅在 type 为 master（主服务器）的情况下存在, 可以写多个具体的 DNS从服务器



**/var/named/目录下的解析文件权限为 root:named ，最好是从模板文件cp出来，否则需要修改组权限**
dns解析文件 /var/named/saintkay.com.zone 如下

~~~
$TTL 1D
@       IN SOA  dns.saintkay.com. rname.invalid. (

                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3D )    ; minimum
        NS      dns.saintkay.com.
dns     A       192.168.1.11
www     A       192.168.1.11
a       A       192.168.1.11
b       A       192.168.1.12
~~~

* 第一个信息是 TTL（Time To Live 的缩写，表示“生存时间”）。当某台电脑去查询你的 DNS 服务器以获取信息时，此信息将被存储在它的 cache（缓存）中（也就是存储在它的 DNS 服务器的内存中，以防止它再次需要信息时重新询问你的 DNS 服务器）。TTL 表示信息保留在 cache 中的时长。超过此时间之后，再次需要信息时就必须对你的 DNS 服务器发出新请求，这里设置为1天
* SOA（Start Of Authority 的缩写，表示“授权的开始”）类型的记录。SOA 类型后面是两条信息。第一个是主域名服务器（master）的名称（此处是 dns.saintkay.com. ），第二个是域名管理员的电子邮件地址（此处是 root.saintkay.com.） ，这里是用点号（.）替换了通常邮件地址中的 @ 符号，因此域名管理员的邮件地址就是 root@saintkay.com ）。接下来，圆括号 () 中包含了不同的值：
  + Serial 表示“序列，序列号”，它里面有你所在区域的版本号。每次修改都应该增加这个版本号。这将告诉你的 DNS 服务器你的区域已更新，并且应该要发送通知到你的从属服务器。建议序列号采用 YYYYMMDDXX 的形式（YYYYMMDD 表示“年月日”。XX 是当前的版本。此处的 20200316 表示“2020年3月16日”；而 01 就是版本号，表示“第 1 版”），这也可以使你知道区域的最新更新日期
  + Refresh 表示“刷新”，是将记录存储在从属服务器上的时长。超过此时间之后，从属服务器将向主服务器请求新的更新。此处是 1D，表示 1天。
  + Retry 表示“重试”，是从属服务器等待重试的时间。也就是如果暂时无法连接到主服务器，再过多少时间重新尝试一次。此处是 1H，表示 1小时。
  + Expire 表示“期满，到期”，是从属服务器持续尝试与主服务器联系的时长。此处是 1w，表示1周。
  + Negative Cache TTL 表示“否定缓存的生存时间”，如果某个 DNS 服务器返回的结果是“你所查询的域名或者数据类型不存在”，则本地 DNS 服务器也会将该信息暂时放入缓存中。此处是 3D，表示 3天。
* SOA 记录的下方是其他主要的记录，分为 4 个部分（有时一些特殊的记录有 5 个部分）
  + 第一列信息是域（domain）的主机，可以选择留空白（指整个域），也可以是 @，或者是机器名称，或者是子域名。
  + 第二列信息代表分级。此处是 IN，表示这是一个和 Internet（Internet 表示“互联网”）有关的记录。IN 是 Internent 的前两个字母。除了 IN，也存在其他值，但是却并不被使用，所以我们总是输入 IN。
  + 第三列信息指定记录的类型
    - A 记录：这是最常见的记录类型，它将一个主机名与一个 IPv4 地址匹配；
    - AAAA 记录：将一个主机名与一个 IPv6 地址匹配；
    - CNAME 记录：用于创建指向另一个主机名的别名（alias）；
    - NS 记录：定义域名的 DNS 服务器；
    - MX 记录：定义域名的邮件服务器
    - PTR 记录：将 IP 对应于主机名，是 A 记录的逆向记录，负责将 IP 反向解析为域名。仅在反向区域中使用
    - SOA 记录：提供区域的信息，例如主 DNS 服务器，区域的管理员的电子邮件地址，区域的序列号，以及我们将详细说明的持续时间。
  + 第四列信息指定记录的值，根据记录的类型不同，值的样式也不同。例如，A 记录的值是 IP 地址，PTR 记录的值是主机名，等等

配置完之后 检查此文件，第一个参数是域，第二个是文件名
~~~
named-checkzone saintkay.com saintkay.com.zone
~~~

## DNS主从服务

dns从服务器为了降低dns主服务器压力

### 主服务器配置

1. 修改 /etc/named.rfc1912.zones
修改allow-update 地址为从服务器地址或者网段
```
allow-update { 192.168.1.21; };
```
### 从服务器配置



1. 修改 /etc/named.rfc1912.zones
   * 修改 type 为 slave
   * 填写主服务器的地址masters
   * 修改file文件保存位置，为slaves下，文件自动生成

```
zone "saintkay.com" IN {
	type slave;
	masters { 192.168.1.20; };
	file "slaves/braineuroo.com.zone";
	allow-update { none; };
};
```

## DNS 缓存服务

dns缓存服务为了加快解析速度
如果记录在缓存中，则直接返回，否则缓存服务器会想主dns服务器获取

1. 安装 dnsmasq
```sh
yum install -y dnsmasq
```
2. 修改配置文件 /etc/dnsmasq.conf
```conf
#dns主服务器地址
server=192.168.1.20
#缓存条数
cache-size=150
#缓存的域名
domain=braineuroo.com
```
3. 启动 dnsmasq
```sh
systemctl enable dnsmasq --now
```

## DNS 分离解析

把同一个域名解析到不同ip

1. 修改配置文件 /etc/named.conf
```conf
#原配置
zone "." IN {
	type hint;
	file "named.ca";
};

#修改为根据不同访问ip解析为不同ip。例如根据电信联通来区分
#分别指向不同的zones文件，原有的 /etc/named.rfc1912.zones 可以注释
view dianxin {
  match-clients { 192.168.1.0/24 };
  zone "." IN {
	  type hint;
	  file "named.ca";
  };
  include "/etc/dianxin.zones"
};

view liantong {
  match-clients { 192.168.2.0/24 };
  zone "." IN {
	  type hint;
	  file "named.ca";
  };
  include "/etc/liantong.zones"
};

#include "/etc/named.rfc1912.zones"
```

2. 配置区域配置文件

复制
```sh
cp -a /etc/named.rfc1912.zones /etc/dianxin.zones
cp -a /etc/named.rfc1912.zones /etc/dianxin.zones
```

例：dianxin.zones
```
zone "saintkay.com" IN {
  type master;
	file "saintkay.com.zone";
	allow-update { none; };
};
```
3. 配置数据配置文件zone

```
$TTL 1D
@	IN SOA	saintkay.com. rname.invalid. (
                    0	; serial
                    1D	; refresh
                    1H	; retry
                    1W	; expire
                    3H )	; minimum
	  NS    dns.saintkay.com.
dns	A	    192.168.1.10

...
添加需要解析的3级域名地址
```

## 其他
域名解析测试命令
```
nslookup 域名
```

