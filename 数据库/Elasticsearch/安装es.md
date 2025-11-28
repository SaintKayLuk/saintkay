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


## Install with Debian Package

文档地址：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/deb.html


安装目录为 /usr/share/elasticsearch
配置目录为 /etc/elasticsearch

##### 准备工作
```sh
# 安装公钥
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

# 下载 7.x 仓库
sudo apt-get install apt-transport-https
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
```

##### 安装
安装 7.x 最新版，目前为 7.17.29
```sh
sudo apt-get update && sudo apt-get install elasticsearch
```

如果网不好，可以手动下载 deb 包来安装
```sh
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.29-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.29-amd64.deb.sha512
# 可以对比一下 sha 的值，最终输出 elasticsearch-{version}-amd64.deb: OK
shasum -a 512 -c elasticsearch-7.17.29-amd64.deb.sha512 
sudo dpkg -i elasticsearch-7.17.29-amd64.deb
```