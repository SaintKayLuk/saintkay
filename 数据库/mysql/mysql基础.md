## mysql版本

* MySQL Community Server (社区版)
* MySQL Enterprise Edition (企业版)
* MySQL Cluster CGE (集群版)




```
mysql [选项]
    --host/-h           指定mysql服务的地址
    --port/-P           (大写)指定端口
    --user/-u           指定用户名，默认root
    --password/-p       指定密码
    --execute/-e        执行一个或者多个sql(多条sql用;分隔)后退出，参数需要双引号


对于长格式，选项和值之间用 = 连接，短格式则不需要，例如 --host=localhost 和 -hlocalhost
但有一个例外，--password=123 和 -p123 ，短格式-p和密码之间没有空格
```


需要交互输入密码
```
mysql_config_editor set -G root -h 192.168.2.203 -u root -p

mysql --login-path=root
```




## 日志文件

二进制日志选项位于 mysqld 下
```conf
[mysqld]
server_id           = 2                 #唯一标识，
log_bin             = [mysql-bin]	    #直接写log_bin开启日志，也指定日志名前缀，默认名是hostname
max_binlog_size     = 512M              #单个日志文件最大值，确保事务在同一日志文件，此文件可能会大于此值 (默认 1G )
expire_logs_days    = 0                 #自动删除binlog日志天数，默认为0，永不删除
binlog_format       = ROW               #ROW(默认)，MIXED，STATEMENT

binlog_do_db = test           #日志记录那些数据库,（不设置同步所有，除了binlog_ignore_db忽略的）
binlog_do_db = test2          #设置多个库，需要分开写，不能写成(binlog_do_db = test,test2) mysql会将 test,test2 认为是一个名为 "test,test2" 的数据库
binlog_ignore_db = mysql  #日志忽略记录得数据库
binlog_ignore_db = performance_schema
binlog_ignore_db = information_schema
binlog_ignore_db = sys
```



```
mysqlbinlog [选项] log_file 
    --stop-position
    --start-position
    
```

```
mysqlbinlog mysql-bin.000001 | mysql -uroot -p123456
```

```sql
--删除当前日志之前的所有日志文件，当前日志文件不删除
PURGE BINARY LOGS TO 'mysql-bin.000010';
```

```
mysqlbinlog --base64-output=decode-rows -v
```



## 配置

修改wait_timeout必须也修改interactive_timeout
```
[mysqld]
wait_timeout=28800
interactive_timeout=28800   
```

## 三种插入数据方式

* INSERT INTO
* REPLACE INTO
* INSERT IGNORE INTO

```
insert into ：插入数据
插入数据时会检查主键（PrimaryKey）或unique索引，如果存在则报错

replace into：覆盖插入数据
插入数据时候，如果存在主键或unique索引相同数据，则覆盖，不存在则新增

insert ignore into：忽略插入数据
插入数据时候，如果存在主键或unique索引相同数据，则忽略，即使其他字段不一致也忽略，不存在则新增数据
```

## 日期时间

* date
* time
* datetime
* time

```
date：YYYY-MM-DD
日期格式，只有日期，没有时间,例如2022年12月12日(2022-12-12)

time：hh:mm:ss[.000000]
时间格式  只有时间没有日期，可以最多带6位小数，例如12点12分12秒带6位小数(12:12:12.666666)

datetime：YYYY-MM-DD  hh:mm:ss[.000000]
日期时间，可以最多带6位小数，不带小数精确到秒，例如 2022年12月12日，12点12分12秒 (2022-12-12 12:12:12)

timestamp YYYY-MM-DD  hh:mm:ss[.000000]
格式和dataetime一样
1. 最大范围到2038年
2. 存储时间会转化为UTC
不建议使用datestamp格式，建议使用datetime
```


## 慢日志查询

```sql
SHOW VARIABLES LIKE '%query%';
```

| Variable_name       | Value                                |
|---------------------|--------------------------------------|
| long_query_time     | 1.000000                             |
| slow_query_log      | ON                                   |
| slow_query_log_file | /var/lib/mysql/55a2340ce0b9-slow.log |


