# HDFS

主从架构

四个组件
* HDFS Client
* NameNode：相当于master
* DataNode：相当于slave
* Secondary NameNode


### client

1. 与NameNode交互，获取文件的位置信息
2. 与DataNode交互，读取/写入文件



## 配置文件

```sh
core-site.xml
hdfs-site.xml
```

**core-site.xml**
```xml

<configuration>

    <!-- namenode的url ，因为会datanode会变成hostname的值得，所以为了能够访问的到，直接把hostname的值改为ip，这样就可以直接访问，对于hdfs来说，这个ip是hostname，对于用户来说，这个ip就能直接访问-->
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://xxx:9000</value> 
    </property>
```

**hdfs-site.xml**
```xml
<configuration>
    <!-- namenode的本地存储路径，不指定，默认在/tmp下 -->
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/xxx</value>
    </property>
    <!-- datanode的本地存储路径，不指定，默认在/tmp下-->
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/xxx</value>
    </property>
    <!-- 文件副本数量，默认3，相当于一份文件会报错3个副本 -->
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>

</configuration>

```


/etc/profile
```
export JAVA_HOME=/opt/jdk-1.8
export PATH=$PATH:$JAVA_HOME/bin 

export HADOOP_HOME=/opt/hadoop-3.3.4 
export JAVA_LIBRARY_PATH=$HADOOP_HOME/lib/native 
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
```

## 启动hdfs

第一次启动，需要对namenode的存储路径格式化
hdfs namenode -format