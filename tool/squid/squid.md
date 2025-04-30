


服务名
```sh
squid
```

配置文件
```sh
/etc/squid/squid.conf
```




## 工作模式

* 传统模式
* 透明模式
* 反向代理

传统代理：在每台电脑上添加代理
透明代理：不需要在每台电脑上添加代理，在网关等位置添加统一代理，对用户无感


### 传统模式

centos 7.x 安装squid
```sh
yum -y install squid  
```

因为默认监听ipv6的3128端口，我们需要改为ipv4
```
vi /etc/squid/squid.conf

...
http_port 3128
改为
http_port 0.0.0.0:3128

```


启动squid
```
systemctl start squid
```



在需要通过代理访问的机器上设置代理 http代理和https代理

```sh
echo "export http_proxy=ip:3128" >> /etc/profile
echo "export https_proxy=ip:3128" >> /etc/profile

 
#重写加载配置文件

. /etc/profile
```

取消代理，相当于取消环境变量
```sh
unset http_proxy
unset https_proxy
```
