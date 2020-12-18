# 配置文件

* 局部：即网卡配置文件，里面只能写一个网卡的dns
```
/etc/sysconfig/network-scripts/ifcfg-eth0

DNS=ip
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


# 

域名解析测试命令
```
nslookup 域名
```





