影响版本：8.5p1 - 9.8p1


两个包
openssh-9.8p1.tar.gz
openssl-1.1.1.tar.gz


## 操作流程


```
./configure --sysconfdir=/usr/local/etc/ssh
./configure --with-ssl-dir=/usr/local/openssl
make install
```