## 系统配置

* es使用非root用户启动
* 禁用swap
* 文件句柄数
* 虚拟内存
* 线程数


文件句柄数：假设使用es用户启动elasticsearch，则在/etc/security/limits.conf中添加以下行
```
es  -  nofile   65535
```


虚拟内存：elasticsearch使用mmapfs一个目录来存索引，linux默认为65536
```sh
#临时设置
sysctl -w vm.max_map_count=262144
#永久设置
echo "vm.max_map_count=262144" >> /etc/sysctl.conf
sysctl -p
```

线程数：elasticsearch使用多个线程池来执行不同类型的操作
在limits.conf中添加
```
es  -  nproc  4096
```


## docker方式

```yaml
version: "3"
services:
  elasticsearch:
    container_name: es
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.11
    ports:
      - 9200:9200
    environment:
      - node-name=node-1
      - discovery.type=single-node
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - /data/elasticsearch/data:/usr/share/elasticsearch/data
```
