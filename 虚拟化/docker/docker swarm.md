# 安装前提

* **安装了Docker的三台Linux主机可以通过网络进行通信**
* **安装了Docker Engine 1.12或更高版本**
* **manager机器的IP地址**
* **主机之间打开端口**

**三个联网主机上**
安装Linux的三台Linux主机，它们可以通过网络进行通信。这些可以是物理机，虚拟机，Amazon EC2实例
虽然说2台也可以组建集群，但是集群一般都是指大于等于3台，不然毫无意义。
其中一台机器是管理员（称为manager1），其中两台机器是工人（worker1和worker2）。

**Docker Engine 1.12或更高**
每个主机上都需要Docker Engine 1.12或更高版本。安装Docker Engine并验证Docker Engine守护程序是否在每台机器上运行

**manager机子的ip**
必须将IP地址分配给主机操作系统可用的网络接口。群中的所有节点都需要通过IP地址连接到manager节点。

**主机之间的开放协议和端口**
以下端口必须可用。在某些系统上，这些端口默认情况下处于打开状态。

* 用于群集管理通信的TCP端口2377
* TCP和UDP端口7946，用于节点之间的通信
* UDP端口4789，用于覆盖网络流量
* 如果计划使用加密（--opt encrypted）创建覆盖网络，则还需要确保允许ip协议50（ESP）流量。

# 基本命令

## docker swarm

集群管理
| 指令                                   | 释义                           |
| -------------------------------------- | ------------------------------ |
| [docker swarm init](#init)             | 初始化一个swarm集群            |
| [docker swarm join](#join)             | 加入swarm集群以work或者manager |
| [docker swarm join-token](#join-token) | 获取加入集群的token            |
| [docker swarm leave](#leave)           | 离开集群                       |

<span id="init">

**docker swarm init**
--advertise-addr  指定manager节点的ip, 如果主机只有一个网卡, 则此选项可以省略, 如果该值为裸IP地址或接口名称, 则将使用默认端口2377。
--availability 节点活性(active|pause|drain), 默认active
--default-addr-pool-mask-length 默认地址池子网掩码长度, 默认24
--force-new-cluster 从当前状态强制创建集群

我们用docker machine来创建一些虚拟docker主机, 然后连接manager1主机创建swarm集群
~~~
$ docker-machine ls
dNAME       ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER     ERRORS
manager1   -        virtualbox   Running   tcp://192.168.99.104:2376           v19.03.5   
manager2   -        virtualbox   Running   tcp://192.168.99.106:2376           v19.03.5 
work1      -        virtualbox   Running   tcp://192.168.99.105:2376           v19.03.5  
$ docker-machine ssh manager1 docker swarm init --advertise-addr 192.168.99.104
Swarm initialized: current node (m0r69wnejsvow63evo9l7plja) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-0g7mfkcdr6fbue3a2ozbmwx0tsodg3ydsyb13blc3v7wns93l8-8ffnuhw9lno2oa7rnkaljanyv 192.168.99.104:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
~~~

上面提示, to add a manager to this swarm, 在manager节点上 执行 docker swarm join-token manager 来获取加入manager节点的命令
</span>

<span id="join">

**docker swarm join**

将节点加入群集。该节点根据您传递的带有--token标记的令牌加入为manager节点或worker节点.[如何获得token值](#join-token)
集群最多只能有3-7个管理器，因为必须有大多数管理器才能使集群正常运行。不应参与此管理仲裁的节点应改为作为工作人员加入。管理器应为具有静态IP地址的稳定主机
--token 加入集群的token值, 必须带上, 此token决定加入的节点作为manager还是worker

~~~
添加work节点
$ docker-machine ssh work1
$ docker swarm join --token SWMTKN-1-0g7mfkcdr6fbue3a2ozbmwx0tsodg3ydsyb13blc3v7wns93l8-8ffnuhw9lno2oa7rnkaljanyv 192.168.99.104:2377
This node joined a swarm as a worker.

添加manager节点
$ docker-machine ssh manager2
$ docker swarm join --token SWMTKN-1-0g7mfkcdr6fbue3a2ozbmwx0tsodg3ydsyb13blc3v7wns93l8-87dqryb3gbfsj3hwe441mlixa 192.168.99.104:2377
This node joined a swarm as a manager.
~~~
</span>

<span id="join-token">

**docker swarm join-token**
--quiet, -q 仅打印令牌, 不显示完整的加入命令

获取token值, 在manager节点上操作, 我们进入manager1节点
~~~
获取以work节点加入的token值
$ docker swarm join-token worker
To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-0g7mfkcdr6fbue3a2ozbmwx0tsodg3ydsyb13blc3v7wns93l8-8ffnuhw9lno2oa7rnkaljanyv 192.168.99.104:2377

获取以manager节点加入的token值
$ docker swarm join-token manager
To add a manager to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-0g7mfkcdr6fbue3a2ozbmwx0tsodg3ydsyb13blc3v7wns93l8-87dqryb3gbfsj3hwe441mlixa 192.168.99.104:2377

~~~

<span>

<span id="leave">

**docker swarm leave**

--force 强制离开swarm, 从swarm中删除manager节点的安全方法是将其降级为worker节点，然后使用leave
docker swarm leave并不会删除节点, 该节点仍将出现在节点列表中，并标记为down。它不再影响群操作，但是一长串down节点会使节点列表混乱。要从列表中删除非活动节点，请使用[node rm](#rm) 命令。

</span>

## docker node

节点管理, 必须在manager节点使用

| Command                            | Description                                      |
| ---------------------------------- | ------------------------------------------------ |
| docker node demote                 | 将一个或多个manager节点降级为worker节点          |
| docker node inspect                | 在一个或多个节点上显示详细信息                   |
| docker node ls                     | 查看swarm中所有节点                              |
| docker node promote                | 将一个或多个worker节点提升为swarm中的manager节点 |
| docker node ps                     | 列出在一个或多个节点上运行的任务，默认为当前节点 |
| [docker node rm](#rm)              | 从swarm中删除一个或多个节点                      |
| [docker node update](#node-update) | 更新节点                                         |

<span id="rm">

**docker node rm**
--force , -f        强制从群中删除节点
docker rm只能从swarm中删除停止的节点
~~~
$ docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
x7ugqpr43skyn8nsctrazkhxc *   manager1            Ready               Active              Leader              19.03.5
dcleaumzh5g01yls3w0yp92jx     work1               Ready               Active                                  19.03.5
$ docker node rm work1                                                                                                                    
Error response from daemon: rpc error: code = FailedPrecondition desc = node dcleaumzh5g01yls3w0yp92jx is not down and can't be removed
~~~
我们尝试从swarm中删除STATUS为Ready的节点, 发现报错, 我们首选要执行[docker swarm leave](#leave)
~~~
$ docker swarm leave
Node left the swarm.

然后进入manger节点操作
$ docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
x7ugqpr43skyn8nsctrazkhxc *   manager1            Ready               Active              Leader              19.03.5
dcleaumzh5g01yls3w0yp92jx     work1               Down                Active                                  19.03.5
$ docker node rm work1                                                                                         
work1
~~~
如果要删除manager节点, 必须将Manager节点降级为Worker节点（使用docker node demote），然后才能将其从集群中删除
</span>

<span id="node-update">

**docker node update**
添加节点标签，在部署服务时非常有用，可以作为约束条件
~~~
$ docker node update --label-add foo=bar worker1
$ docker node update --label-rm foo worker1
~~~

</span>

## docker secret

|Command	                            |Description                                        |
|---------------------------------------|---------------------------------------------------|
|docker secret create	                |Create a secret from a file or STDIN as content    |
|docker secret inspect	                |Display detailed information on one or more secrets|
|docker secret ls	                    |List secrets                                       |         
|docker secret rm	                    |Remove one or more secrets                         |

## docker config

|Command	                            |Description                                        |
|---------------------------            |---------------------------------------------------|
|[docker config create](#config-create)	|Create a config from a file or STDIN               |
|docker config inspect	                |Display detailed information on one or more configs|
|docker config ls	                    |List configs                                       |
|docker config rm	                    |Remove one or more configs                         |

<span id="config-create">

**docker config create**

~~~
docker config create redis redis.conf
创建一个名为redis的配置文件，配置文件内容为当前路径下的redis.conf文件
~~~

</span>

## docker service

| Command                                  | Description                                          |
| ---------------------------------------- | ---------------------------------------------------- |
| [docker service create](#service-create) | Create a new service                                 |
| docker service inspect                   | Display detailed information on one or more services |
| docker service logs                      | Fetch the logs of a service or task                  |
| docker service ls                        | 列出所有服务                                         |
| [docker service ps](#service-ps)         | 列出服务中的任务                                     |
| docker service rm                        | 删除一个或多个服务                                   |
| docker service rollback                  | Revert changes to a service's configuration          |
| [docker service scale](#service-scale)   | 扩展一个或多个副本服务                               |
| docker service update                    | Update a service                                     |

<span id="service-create">

**docker service create**

* --name            服务名称
* --replicas        任务数
* --config          指定要向服务公开的配置

</span>

<span id="service-ps">

**docker service ps**
以下命令显示了redis服务中的所有任务
~~~
$ docker service ps redis                                                                         
ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
fle8hqjbzd0g        redis.1             redis:latest        manager1            Running             Running 51 seconds ago                       
87wnzvyl87l8        redis.2             redis:latest        work1               Running             Running 51 seconds ago                       
zvpgdliye6q3        redis.3             redis:latest        work1               Running             Running 51 seconds ago    
~~~

</span>

<span id="service-scale">

**docker service scale**
我们有3个redis节点, 我们扩展到5个
~~~
$ docker service ps redis                                                                      
ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE                ERROR               PORTS
2x4z604hbt9b        redis.1             redis:latest        manager1            Running             Running about a minute ago                       
pm5ldwil2ivo        redis.2             redis:latest        worker1             Running             Running 13 seconds ago                           
jqcu0n5cooxw        redis.3             redis:latest        worker1             Running             Running 13 seconds ago   

$ docker service scale redis=5                                                                            
redis scaled to 5
overall progress: 5 out of 5 tasks 
1/5: running   [==================================================>] 
2/5: running   [==================================================>] 
3/5: running   [==================================================>] 
4/5: running   [==================================================>] 
5/5: running   [==================================================>] 
verify: Service converged 

$ docker service ps redis                                                                                        
ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
2x4z604hbt9b        redis.1             redis:latest        manager1            Running             Running 2 minutes ago                        
pm5ldwil2ivo        redis.2             redis:latest        worker1             Running             Running 2 minutes ago                        
jqcu0n5cooxw        redis.3             redis:latest        worker1             Running             Running 2 minutes ago                        
mgfvwvz4saj6        redis.4             redis:latest        manager1            Running             Running 33 seconds ago                       
uqwzl0jrgs0g        redis.5             redis:latest        manager1            Running             Running 33 seconds ago   
~~~

</span>

## docker stack

| Command               | Description                                    |
| --------------------- | ---------------------------------------------- |
| docker stack deploy   | Deploy a new stack or update an existing stack |
| docker stack ls       | List stacks                                    |
| docker stack ps       | List the tasks in the stack                    |
| docker stack rm       | Remove one or more stacks                      |
| docker stack services | List the services in the stack                 |
