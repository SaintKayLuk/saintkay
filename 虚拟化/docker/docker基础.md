# 底层技术

* namespace：进程隔离
* cgroup：资源限制/隔离
* rootfs：容器文件系统，容器根目录相当于一个系统根目录
* Union File System(联合文件系统)：镜像分层技术，将多个目录挂载到一起


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


## 导入导出镜像和容器
### save 和 load

针对镜像的导入和导出

* save：将一个或者多个镜像打包成tar文件
```sh
docker save [选项] image [image ...]
    --output，-o
```
```sh
例：将abc:1.1镜像打包成 abc.tar
docker save -o abc.tar abc:1.1
docker save abc:1.1 > abc.tar

例：将abc:1.1 和 bcd:2.2 镜像打包并且通过gzip压缩成 aaa.tar.gz
docker save abc:1.1 bcd:2.2 | gzip > aaa.tar.gz
```

也可以打包容器名，但是打包的是容器对应的镜像

* load：将save打包的镜像文件恢复成镜像

```sh
docker load [选项] xxx.tar
    --input,-i
```

```sh
例：将 abc.tar 导入成镜像
docker load -i abc.tar
docker load < abc.tar
```
可以直接导入通过gzip压缩的镜像文件

### export 和 import

针对容器的导入和导出，export 将容器的文件系统导出为 tar 存档，不会导出与容器关联的卷的内容，import也会把通过export导出的tar存档导入为镜像

* export
```
docker export [选项] 容器名 
    --output，-o
```

```
例：将容器 abc 导出为 abc.tar
docker export abc  > abc.tar
docker export --output="abc.tar" abc
```

* import

导入一个文件系统的tar存档并可以重新命名

```
docker import [选项] [file/url/-] [REPOSITORY[:TAG]]
    --change，-c
    --message，-m
```

```
例：通过管道和输入导入一个 abc.tar 并命名为 test:1.1
cat abc.tar | docker import - test:1.1
例：导入本地文件 abc.tar
docker import abc.tar 
```

