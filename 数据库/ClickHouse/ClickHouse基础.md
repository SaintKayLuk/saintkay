##  clickhouse

* clickhouse-server(服务端)
* clickhouse-client(命令行客户端)

端口
```
8123    http端口
9000    tcp端口
9004    mysql连接端口
```



### 配置文件

server端配置文件
```conf
/etc/clickhouse-server/                 #配置文件目录
/etc/clickhouse-server/config.d/        #自定义配置文件目录
/etc/clickhouse-server/config.xml       #主配置文件
/etc/clickhouse-server/users.d/         #用户相关配置文件自定义目录
/etc/clickhouse-server/users.xml        #用户相关配置文件
```

client端配置文件
```conf
/etc/clickhouse-client/config.xml       #客户端配置文件
```


```
clickhouse [选项]
    status  查看状态
    start   启动
    stop    停止
    restart 重启
```

```
clickhouse-client [参数]
    --host,-h       
    --port          连接端口，(默认值：9000)
    --user,-u       用户名，(默认值：default)
    --password      密码，(默认：空字符串)
    --query,-q      非交互查询
    --database,-d   默认当前操作数据库，默认值：default
    --multiline,-m  如果指定，允许多行语句查询(enter仅代表换行，分号代表语句结束)
    --multiquery,-n 
    --format,-f
    --time,-t
    --stacktrace
    --config-file
    --secure
    --history_file
    --param_<name>
```








### 数据类型

#### UUID

通过generateUUIDv4()函数生成UUID

格式：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
未指定：00000000-0000-0000-0000-000000000000

#### 整数类型

* Int8：8位，1字节，从-128到127
* Int16
* Int32
* Int64
* UInt8：8位，1字节，无符号，从0到255
* UInt16
* UInt32
* UInt64 

#### 浮点类型

* Float32：相当于其他语言的float 
* Float64：相当于其他语言的double


#### 字符串类型

* String：可变长度
* FixedString：固定长度，如果插入超过固定长度的字节则会报错

#### 时间类型

* Date：年-月-日 例如 2020-02-02
* Datetime：年-月-日 时:分:秒 例如 2020-02-02 12:12:12
* Datetime64 年-月-日 时:分:秒.毫秒 例如 2020-02-02 12:12:12.222

#### Decimal

固定小数位，舍弃多余的小数，定长，超过总长度会报错

* Decimal32：最多9位
* Decimal64
* Decimal128

例：Decimal32(3) 表示小数最多3位，整数部分最多6位，相当于 Decimal(9,3)

#### 其他

clickhouse没有单独的布尔类型，推荐使用 UInt8类型，取值限制 0 或 1 来区分

