# DHCP

动态主机配置协议

## 租约四部曲

1. dhcp客户机将自己的ip设置成0.0.0.0 ，以0.0.0.0为源地址，255.255.255.255为目标地址，使用udp67端口为目标端口发送广播请求 DHCP DISCOVER 帧
2. DHCP 服务器收到 dhcp客户机的请求，在自己的地址池查找合法的ip地址，将此ip做上标记，使用udp68作为源端口广播发送 DHCP OFFER 帧，包括 dhco客户机的mac地址，dhcp服务器提供的 IP 地址，子网掩码，以及默认网关的 IP 地址， DNS 服务器的 IP 地址等
3. dhcp客户端从第一个收到的 DHCP OFFER帧中 选择ip地址，并以为0.0.0.0为源地址，255.255.255.255为目标地址使用udp67端口为目标端口来广播 HCP REQUEST 帧来表明接受提供的内容
4. dhcp服务器收到 DHCP REQUEST 消息后，发送 DHCP ACK 帧，以确认 “租约”（lease）的分配。

DHCP服务器分配的IP地址（还有关联的子网掩码，等等）是有期限的。过了期限之后，必须重新请求一个IP地址。不过，要续订 “租约”（重新请求一个 IP 地址）时，客户端不需要进行从 DHCP DISCOVER 开始的整个过程，而是直接从 DHCP REQUEST 开始。DHCP 服务器会把与 MAC 地址关联的已分配的 IP 地址保存在内存中。因此，即使你的 “租约” 确实已续签多次，你有时仍会保留相同的 IP 地址很长时间。
~~~

1. client ---> DHCP DISCOVER        ---> ff:ff:ff:ff:ff:ff
2. client <--- DHCP OFFER           <--- dhcp server
3. client ---> DHCP REQUEST         ---> ff:ff:ff:ff:ff:ff
4. client <--- DHCP ACK / DHCP NAK  <--- dhcp server

~~~ 

## dhcp续租

正常续租
```
租约四部曲
...
租期50%
clinet --> DHCP REQUEST --> dhcp server
client <-- DHCP ACK/NAK <-- dhcp server
更新租期
```

dhcp客户端在租期过去 50% 的时候，会向提供ip地址的dhcp服务器发送 DHCP REQUEST 请求，如果接收到 DHCP ACK 回应，则更新租期，如果没有收到dhcp服务器的响应，则继续使用当前ip，并在租期过去 87.5% 的时候再次向提供ip地址的dhcp服务器发送DHCP REQUEST请求，如果还没有响应，则在租期到 100% 的时候，dhcp客户机使用 169.254.0.0/16 中的随机一个地址，并每5分钟进行尝试 dhcp

续租不成功
```
租约四部曲
...
租期 50%
clinet --> DHCP REQUEST --> dhcp server
租期 87.5%
clinet --> DHCP REQUEST --> dhcp server
租期 100% --> 选择 169.254.0.0/16 中一个地址
5分钟
client ---> DHCP DISCOVER ---> ff:ff:ff:ff:ff:ff
```
