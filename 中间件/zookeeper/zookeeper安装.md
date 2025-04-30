## 直接部署，单机模式

1. 先安装jdk
2. 下载 apache-zookeeper-3.5.10-bin.tar.gz [下载地址](https://archive.apache.org/dist/zookeeper/zookeeper-3.5.10/)
3. 解压
4. 修改配置文件
5. 启动

最简单的配置文件
```conf
clientPort=2181
dataDir=/tmp/zookeeper
```

## 直接部署，集群模式

集群配置文件
```conf
tickTime=2000
dataDir=/tmp/zookeeper
clientPort=2181
initLimit=5
syncLimit=2
server.1=zoo1:2888:3888
server.2=zoo2:2888:3888
server.3=zoo3:2888:3888
```

其中 zoo1，zoo2，zoo3 是指3台zk的host，要能够访问到的host
根据server.1 的这个1 分别去每台几点的 dataDir下创建 myid文件，文件内容为 配置文件里的 1，2，3
