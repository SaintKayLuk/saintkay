apt update
apt install -y pgpool2






## 源码安装




```sh
apt install libpq


./configure --prefix=/opt/pgpool2
make
make install
```




### 配置

**pcp.conf** 配置

```sh
cp $prefix/etc/pcp.conf.sample $prefix/etc/pcp.conf


pg_md5 your_password

# 然后在 pcp.conf 文件中添加一行,前面是数据库的用户名，后面是 通过pg_md5 加密的密码
# USER:PASSWORD
```


**pgpool.conf**配置


```conf
backend_clustering_mode = 'streaming_replication'

# 设置 * 则同时监听 ipv4 和 ipv6 ，设置 0.0.0.0 则只监听 ipv4
listen_addresses = '0.0.0.0'
pcp_listen_addresses = '0.0.0.0'



```



### 启动

可能报错项

```sh
# could not open pid file "/var/run/pgpool/pgpool.pid"
# no such file or directory

# 手动创建一下目录就行

mkdir /var/run/pgpool
```



