## 安装containerd


1. 下载，解压
```sh
#下载地址
https://github.com/containerd/containerd/releases

#下载具体版本文件，此文件自带了cri 和 containerd.service 和 cni
wget https://github.com/containerd/containerd/releases/download/v1.4.13/cri-containerd-cni-1.4.13-linux-amd64.tar.gz
```

**单独使用containerd的时候下载带cni的包，如果把containerd当k8s的运行时，下载单独的包，手动安装 cni**

删除 /etc/cni/net.d 下默认cni配置


解压到对应目录,默认就给我们分好目录了，直接解压到 /，会自动解压到对应目录
```sh
tar -zxvf cri-containerd-cni-1.4.13-linux-amd64.tar.gz -C /


etc/crictl.yaml
...
etc/systemd/system/containerd.service
...
usr/local/
...
opt/cni/
...
opt/containerd/
...

#crictl.yaml：runtime默认连接点配置，没有此配置文件会先找 dockershim.sock
```


2. 修改默认pause镜像地址
```sh
#默认配置
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml


vi /etc/containerd/config.toml

sandbox_image = "k8s.io/pause:3.6"
        ↓改为↓
sandbox_image = "registry.aliyuncs.com/google_containers/pause:3.2"
```

3. 重新加载contarinerd
```
systemctl daemon-reload
systemctl enable containerd --now
```

4. 验证一下
```
[root@k8s-1 ~]# ctr version
Client:
  Version:  1.6.4
  Revision: 212e8b6fa2f44b9c21b2798135fc6fb7c53efc16
  Go version: go1.17.9

Server:
  Version:  1.6.4
  Revision: 212e8b6fa2f44b9c21b2798135fc6fb7c53efc16
  UUID: be15f1ad-d970-4b12-9272-a418a664b45c

```


## 卸载containerd

因为是直接解压的，所以需要手动删除


取消开机自启，并停止
```sh
systemctl disable containerd --now

# 可选，删除service文件，版本跨度过大，service文件有可能不同
rm -f  /lib/systemd/system/container*
```


删除文件
```sh
rm -f  /etc/crictl.yaml
rm -rf /etc/containerd
rm -rf /opt/containerd

# 如果安装了其他的软件，则手动删除，如果没有其他软件，则直接全都删除c开头的
rm -rf /usr/local/bin/c*
rm -rf /usr/local/sbin/runc

rm -rf /var/lib/containerd /run/containerd

```