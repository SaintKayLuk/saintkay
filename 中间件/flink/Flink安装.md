## 下载地址

```
https://flink.apache.org/zh/downloads.html
```


flink 1.13.6，scala 2.12 版本
```sh
https://archive.apache.org/dist/flink/flink-1.13.6/flink-1.13.6-bin-scala_2.12.tgz
```

```sh
flink-1.13.6
    ├── bin             #可执行文件
        ├── bash-java-utils.jar
        ├── config.sh
        ├── find-flink-home.sh
        ├── flink
        ├── flink-console.sh
        ├── flink-daemon.sh
        ├── historyserver.sh
        ├── jobmanager.sh
        ├── kubernetes-jobmanager.sh
        ├── kubernetes-session.sh
        ├── kubernetes-taskmanager.sh
        ├── pyflink-shell.sh
        ├── sql-client.sh                   #启动sql客户端
        ├── standalone-job.sh
        ├── start-cluster.sh                #启动集群
        ├── start-zookeeper-quorum.sh
        ├── stop-cluster.sh                 #停止集群
        ├── stop-zookeeper-quorum.sh
        ├── taskmanager.sh
        ├── yarn-session.sh
        └── zookeeper.sh
    ├── conf            #配置文件
    ├── examples        #一些示例任务
    ├── lib             #flink依赖的jar包
    ├── log             #日志文件
    ├── opt             #flink自己的jar包
    ├── plugins         #插件
```


## 单机模式
```sh
cd flink-1.13.6
#启动集群
./bin/start-cluster.sh

#停止集群
./bin/stop-cluster.sh
```







