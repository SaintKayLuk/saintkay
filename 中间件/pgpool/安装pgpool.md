






## 源码安装

```sh
apt install libpq-dev


./configure --prefix=/opt/pgpool2
make
make install
```




### 配置


环境变量配置，pgpool 命令添加到环境变量中


```sh
echo 'export PATH="$PATH:/opt/pgpool2/bin"' >> ～/.bashrc
source ～/.bashrc
```

**pcp.conf** 配置

```sh
cp $prefix/etc/pcp.conf.sample $prefix/etc/pcp.conf


pg_md5 your_password

# 然后在 pcp.conf 文件中添加一行,前面是数据库的用户名，后面是 通过pg_md5 加密的密码
# USER:PASSWORD
```





### 启动

可能报错项

```sh
# could not open pid file "/var/run/pgpool/pgpool.pid"
# no such file or directory

# 手动创建一下目录就行

mkdir /var/run/pgpool
```

启动与停止
```sh
# 启动
pgpool -f /opt/pgpool2/etc/pgpool.conf -F /opt/pgpool2/etc/pcp.conf

# 停止
pgpool -f /opt/pgpool2/etc/pgpool.conf -F /opt/pgpool2/etc/pcp.conf -m fast stop
```


