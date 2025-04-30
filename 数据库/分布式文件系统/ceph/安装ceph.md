# 安装ceph

推荐两种方式
* cephadm：容器化的方式部署，15.x版本以上
* rook：k8s环境下的部署，需要k8s环境

## cephadm方式
安装docker
添加yum源

地址为https://download.ceph.com
根据linux版本自行修改地址

安装15.2.17版本
```sh
cat >/etc/yum.repos.d/ceph.repo << EOF
[Ceph]
name=Ceph packages for $basearch
baseurl=https://download.ceph.com/rpm-15.2.17/el7/x86_64/
enabled=1
gpgcheck=0
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
priority=1

[Ceph-noarch]
name=Ceph noarch packages
baseurl=https://download.ceph.com/rpm-15.2.17/el7/noarch
enabled=1
gpgcheck=0
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
priority=1

[ceph-source]
name=Ceph source packages
baseurl=https://download.ceph.com/rpm-15.2.17/el7/SRPMS
enabled=1
gpgcheck=0
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
EOF
```

安装cephadm
```sh
yum install -y cephadm
```

修改主机名
```sh
#如果只有一台则修改自己的主机名即可
hostnamectl set-hostname ceph-1
#如果有多台服务器，每台修改完主机名之后，在 /etc/hosts 下添加对应的主机，或者使用 私有dns服务器
```

```sh
#使用cephadm初始化集群
cephadm bootstrap --mon-ip <mon-ip> --config <ceph.conf>
    --mon-ip <mon-ip>       #指定mon服务的ip 
    --config <ceph.conf>   #指定初始配置文件

# 运行一个可执行ceph的容器
# 如果在有mon的主机上运行 cephadm shell ，则 /etc/ceph 目录下是 mon 容器的内容
# 如果在没有mon的主机上运行，则 /etc/ceph 目录下是宿主机的内容
cephadm shell 
```


```sh
#查看设备列表
ceph orch device ls
```

```sh
#删除集群，指定fsid
cephadm rm-cluster --fsid xxx --force
```











### 

```sh
#移除一个被使用过的硬盘，可以被ceph重新使用
ceph-volume lvm zap </dev/sdc> --destroy
```

### 其他

```sh
#归档报警信息
ceph crash archive-all
```