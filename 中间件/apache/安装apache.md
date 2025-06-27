## 编译安装


```sh
sudo yum groupinstall "Development Tools"
sudo yum install gcc gcc-c++ make pcre pcre-devel openssl-devel expat-devel
```


安装最新版本，版本可能会变化
```sh
wget https://downloads.apache.org/httpd/httpd-2.4.59.tar.gz
wget https://downloads.apache.org/apr/apr-1.7.6.tar.gz
wget https://downloads.apache.org/apr/apr-util-1.6.3.tar.gz
```




```sh
tar -xzf httpd-2.4.59.tar.gz
tar -xzf apr-1.7.6.tar.gz
tar -xzf apr-util-1.6.3.tar.gz

mv apr-1.7.6 httpd-2.4.59/srclib/apr
mv apr-util-1.6.3 httpd-2.4.59/srclib/apr-util
cd httpd-2.4.59
```

```sh
./configure --prefix=/opt/apache2.4 --enable-so --enable-ssl --with-mpm=event --enable-mods-shared=all
make -j$(nproc)
sudo make install
```

