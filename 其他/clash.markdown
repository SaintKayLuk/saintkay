## 情景1

同时连接网线和无线
网线为内网，无线为互联网

内网有dns服务器，访问内网的域名，因为 clash 会接管本地 dns，所以需要修改配置



1. 订阅里 -> 右键当前订阅 -> 编辑文件

```yaml
...
dns:
  enable: true
  ipv6: false
  default-nameserver:
    - 192.168.1.1                   # 添加这一行，内网dns地址
    - 223.5.5.5
    - 119.29.29.29
    - 114.114.114.114
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  use-hosts: true
  nameserver:
    - 192.168.1.1                   # 添加这一行，内网dns地址
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
    - tls://223.5.5.5:853
    - tls://223.6.6.6:853
    - 114.114.114.114
  hosts:                            # 添加这两行
    "xxx.xxx.com": 192.168.1.123    # 内网地址映射关系
...
```


2. 订阅里 -> 编辑规则 -> 规则类型 DOMAIN -> 规则内容为内网域名 -> 代理策略为 DIRECT



