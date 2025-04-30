# 安装docker


## centos7
https://docs.docker.com/engine/install/centos/

### 通过存储库安装

* 卸载旧版本
~~~
yum remove docker*
~~~

* 安装yum-utils包
~~~
yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
~~~

* 设置存储库
~~~
官网-比较慢
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo


阿里云源
yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo


清华大学源
yum-config-manager \
    --add-repo \
    https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/centos/docker-ce.repo
~~~

* 安装最新版本
~~~
yum install -y docker-ce docker-ce-cli containerd.io
~~~

* 安装特定版本
~~~
列出可用版本
yum list docker-ce --showduplicates | sort -r

docker-ce.x86_64            3:19.03.9-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.8-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.7-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.6-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.5-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.4-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.3-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.2-3.el7                     docker-ce-stable
...

安装特定版本
yum install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io
VERSION_STRING为第二列冒号后面到分隔符 - 为止
例如 docker-ce-19.03.8
~~~

以VERSION_STRING = **19.03.9**为例
```shell
yum install -y docker-ce-19.03.9 docker-ce-cli-19.03.9 containerd.io
```

### 通过包安装

1. 直接下载
   1. 下载地址：https://download.docker.com/linux/centos/
   2. 并选择您的 CentOS 版本。然后浏览x86_64/stable/Packages/
2. 通过yum下载rpm包
   1. yum install --downloadonly --downloaddir=/tmp docker-ce-19.03.8 docker-ce-cli-19.03.8 containerd.io
   2. 到/tmp目录下把rpm包拷贝到需要通过包安装的机器


### 通过二进制文件安装

下载地址：https://download.docker.com/linux/static/stable/

例：安装 docker-19.03.8
```sh
tar -zxvf docker-19.03.8.tgz   

移动解压文件到/usr/bin下(可选)
mv docker/* /usr/bin/    

添加docker.service
vim /usr/lib/systemd/system/docker.service


systemctl start docker
```

docker.service内容
```sh
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
```




## 卸载docker

yum remove docker-ce docker-ce-cli containerd.io



## ubuntu


卸载旧包
```sh
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

设置存储库
```sh
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```


国内 https://download.docker.com/linux/ubuntu 可能访问不到，则可以通过包来安装
```sh
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

查看具体版本
```sh
apt-cache madison docker-ce | awk '{ print $3 }'
```

安装具体版本，版本根据上面 madison 出来的版本
```sh
VERSION_STRING=xxx
sudo apt-get install -y docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
```


## ubuntu 通过包安装

1. 下载包，地址
```
https://download.docker.com/linux/ubuntu/dists/
```
1. 选择您的 Ubuntu 版本，并到pool/stable/下
2. 下载以下包
```
containerd.io_<version>_<arch>.deb
docker-ce_<version>_<arch>.deb
docker-ce-cli_<version>_<arch>.deb
docker-buildx-plugin_<version>_<arch>.deb
docker-compose-plugin_<version>_<arch>.deb
```
3. 安装
```sh
sudo dpkg -i *.deb
```
4. 自启并启动
```sh
systemctl enable docker --now
```



# 修改配置

修改配置文件，如果不存在，新建一个
docker配置文件: /etc/docker/daemon.json
[daemon.json](daemon.json)



修改daemon.json配置文件后，需要重新加载，和重启，保证配置文件生效
~~~
systemctl daemon-reload
systemctl enable docker --now
~~~


开启docker api远程访问
~~~sh
/usr/lib/systemd/system/docker.service
/etc/systemd/system/docker.service

ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock
-H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
~~~


设置docker代理
```sh
在docker.service文件的[Service]下添加一行代理设置

/usr/lib/systemd/system/docker.service

[Service]
...
Environment="HTTP_PROXY=ip:port/" "HTTPS_PROXY=ip:port/"
```






