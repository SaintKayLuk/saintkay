## Elasticsearch

* 分布式
* RESTful风格
* 文档型数据库，存储格式为JSON
* 9300 端口为 Elasticsearch 集群间组件的通信端口
* 9200 端口为访问的 http 协议 RESTful 端口


## 目录结构

* LICENSE.txt
* NOTICE.txt
* README.asciidoc
* bin/                
* config/             
  *    elasticsearch.yml
  *    jvm.options
  * log4j2.properties
* data/              
* jdk/                
* lib/                
* logs/               
* modules/
* plugins/            



## 概念

* 索引：一个es中有多个索引，一个索引下有多个文档
  * settings：定义数据分布，例如分片、副本等
  * mappings：定义文档字段类型
* 类型：7.x之后只支持一种，默认 _doc
* 文档：就是一个json格式的内容，相当于一条数据
* 字段
* 映射
* 主分片：一个索引分成几个分片，分开存储，创建索引默认1分片1副本，例如2分片的时候新增一条数据只能存在于某个分片内
  * 一个分片就是一个运行的lucene实例
  * 主分片数在索引创建时指定，后续不可更改，除非reindex
* 副本：顾名思义，一个分片的备份，不能在同一节点上，如果一个索引2个分片2个副本，则一共有4个分片，其中2个主分片，2个副本分片
  * 副本分片数可以动态调整

## 插件

```
bin/elasticsearch-plugin
    list        查看已安装插件
    install     安装插件
    remove      删除插件
```


## 监控工具

* cerebro


## 读写数据流程

假设有3个节点，node-1，node-2，node-3，一个索引user，3分片(P0,P1,P2)1副本(R0,R1,R2),

```
node-1  P0  R2
node-2  P1  R0
node-3  P2  R1
```

### 写数据

1. 客户端向node-1发起写数据请求
2. node-1通过路由计算，该数据应该存到P1分片，node-1向node-2发送存数据请求
3. node-2上的P1主分片写完数据，并向node-3上的R1副本发送数据
4. node-3上的副本写完数据反馈给node-2
5. node-2得到副本的反馈，并反馈给node-1
6. node-1反馈客户端，写数据完成


写数据参数，是否让所有副本都写完数据再返回，或者是能否写成功

| 参数        | 含义                                                                                    |
|-------------|---------------------------------------------------------------------------------------|
| consistency | 一致性，取值one(所有主分片正常)，all(主分片和副本都正常写完)，quorum(大多数副本分片都写完) |
| timeout     | 没有足够多的副本则等待，最多等待1分钟，100表示100毫秒，30s表示30秒                         |
### 读数据












