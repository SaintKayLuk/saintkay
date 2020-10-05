# 安装docker(centos 7)
https://docs.docker.com/engine/install/centos/
卸载旧版本
~~~
yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
~~~


~~~
yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
~~~

添加yum源
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

## 安装最新版本
~~~
yum install -y docker-ce docker-ce-cli containerd.io
~~~

## 安装特定版本
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
例如
docker-ce-19.03.8
~~~

以VERSION_STRING = **19.03.8**为例
yum install -y docker-ce-19.03.8 docker-ce-cli-19.03.8 containerd.io


# 卸载docker

yum remove docker-ce docker-ce-cli containerd.io


# 修改配置

修改配置文件，如果不存在，新建一个
docker配置文件: /etc/docker/daemon.json
[daemon.json](daemon.json)



修改daemon.json配置文件后，需要重新加载，和重启，保证配置文件生效
~~~
systemctl daemon-reload
systemctl start docker
systemctl enable docker
~~~
~~~

开启docker api远程访问
/usr/lib/systemd/system/docker.service
~~~
-H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
~~~

# 常用命令

| Command        | Description |
|----------------|-------------|
| docker run     | 启动一个单独的容器  |
| docker-compose | 一台机器多个服务    |
| docker service | 多台机器一个服务    |
| docker stack   | 多台机器多个服务    |

docker指令 只需要安装docker engine就行
docker-compose需要安装docker-compose插件
docker service 和docker stack需要在docker swarm的manager节点上 


修改容器时区为 CST+8
docker cp /usr/share/zoneinfo/Asia/Shanghai 容器名:/etc/localtime