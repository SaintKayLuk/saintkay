ufw 和 firewalld 不一样的一点是，systemctl 启动他之后，还需要 ufw enable 来启用，
所以 有可能 systemctl status ufw 是active ，但是 ufw status 是 inactive


#### 关闭 UFW 的 IPv6

```sh
vi /etc/default/ufw

IPV6=yes
# 改为
IPV6=no
```

重启
```sh
ufw reload
```




例：网段 192.168.35.0/24 访问5432端口放行
```sh
sudo ufw allow from 192.168.35.0/24 to any port 5432 proto tcp
```