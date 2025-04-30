# redis


| 功能/特性  | Redis Community      | Redis Stack                        | Redis Enterprise               |
| ---------- | -------------------- | ---------------------------------- | ------------------------------ |
| 核心功能   | 键值存储、缓存、队列 | Redis Community + JSON、搜索等模块 | Redis Stack + 企业级功能       |
| 模块支持   | 基本模块             | JSON、Search、Graph、Bloom 等模块  | 完全支持，且优化性能           |
| 高可用性   | 基本主从复制         | 基本主从复制                       | 多活集群、自动故障转移         |
| 水平扩展   | 不支持               | 不支持                             | 支持动态分片、集群扩展         |
| 企业安全性 | 基本 ACL             | 基本 ACL                           | LDAP 集成、TLS 加密            |
| 存储选项   | 内存                 | 内存                               | 内存+磁盘混合存储              |
| 适用场景   | 缓存、简单存储       | 搜索、分析、时间序列等复杂应用     | 全球分布、超大规模和高可用系统 |



部署模式对比
| 模式                | 高可用性 | 数据分片 | 自动故障恢复     | 适用场景                         |
| ------------------- | -------- | -------- | ---------------- | -------------------------------- |
| 单机模式            | ✘        | ✘        | ✘                | 开发、测试                       |
| 主从复制模式        | ✘        | ✘        | ✘（需 Sentinel） | 读多写少的应用                   |
| Sentinel模式        | ✔        | ✘        | ✔                | 高可用性要求较高的小型系统       |
| 集群模式            | ✔        | ✔        | ✔                | 大规模数据存储和高可用需求       |
| 哨兵 + 集群混合模式 | ✔        | ✔        | ✔                | 需要大规模数据和高可用的复杂系统 |



## 安装redis

```
#可以把链接中5.0.8换成其他版本
curl -O http://download.redis.io/releases/redis-5.0.8.tar.gz
tar -zxf redis-5.0.8.tar.gz
cd redis-5.0.8
#存在Makefile，直接make编译，需要安装gcc
make
#redis-server redis-cli等都在src下
cd src
```

## redis-cli

自带redis客户端，默认连接本地 127.0.0.1:6379 的redis
```
./redis-cli
    -h 主机名   指定要连接的redis的地址，可以用ip也可以用主机名
    -a 密码     如果，redis有密码，则需要密码连接
    -p 端口     如果不是默认6379端口，则需要指定端口
    --raw       utf-8编码显示，显示中文

例：连接ip为11.22.33.44，端口为6666，密码为123456的redis
./redis-cli -h 11.22.33.44 -p 6666 -a 123456


不输密码直接登陆之后，操作也需要用到密码,则继续输入密码
127.0.0.1:6379> auth <password>
OK
```

停止redis也用redis-cli
```
./redis-cli shutdown
```

## redis-server

```
./redis-server
    -port 端口
```

## 配置

* 配置文件 redis.conf
* 运行时配置
  * config get
  * config set




启动时可以指定 redis.conf 不指定默认配置文件
```
./redis-server redis.conf
```
可以通过 config set在redis运行时修改配置文件，等同于redis.conf的配置。但是如果重启，会重新读取redis.conf的配置


通过redis-cli登陆redis可以查看哪些哪些配置
```
./redis-cli 
#查看redis端口
127.0.0.1:6379> config get port 
1) "port"
2) "6379"

#查看所有配置
127.0.0.1:6379> config get *
1) "dbfilename"
2) "dump.rdb"
3) "requirepass"
4) ""
5) "masterauth"
6) ""
...
```

也可以通过 config set 来修改配置参数
```
#设置日志输出级别
127.0.0.1:6379> config get loglevel
1) "loglevel"
2) "notice"
127.0.0.1:6379> config set loglevel debug
OK
127.0.0.1:6379> config get loglevel
1) "loglevel"
2) "debug"
```



## 其他

Redis支持多个数据库，并且每个数据库的数据是隔离的不能共享，并且基于单机才有，如果是集群就没有数据库的概念。

每个数据库对外都是一个从0开始的递增数字命名，Redis默认支持16个数据库（可以通过配置文件支持更多，无上限），可以通过配置databases来修改这一数字。客户端与Redis建立连接后会自动选择0号数据库，不过可以随时使用SELECT命令更换数据库，如要选择1号数据库：
```
127.0.0.1:6379> select 1
OK
127.0.0.1:6379[1]> 
```
多个数据库之间并不是完全隔离的，比如FLUSHALL命令可以清空一个Redis实例中所有数据库中的数据



查看信息，例如是否集群等，集群配置
```
127.0.0.1:6379> info
```