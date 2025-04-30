## 表结构


一个表 Table 可以分为多个分区 Partition ，每个分区内可以分成多个分桶 Tablet，每个分桶可以有多个副本

副本数 replication_num 为每个分桶数量，例如 replication_num = 1 则每个分桶只有自己一份，和ES不同的是 ES 副本数会加上主分片 

总Tablet数 = 分区数 * 分桶数 * 副本数

* 分区

非必须，不分区则一张表是一个分区
一张表可以分成多个分区，分区键只支持整数和日期


* 分桶

建表必须，一张表必须分桶
每个分区内，根据某一列或者某几列 分桶

**建议分桶数量 = BE节点数量 * CPU 核数/2**


### 数据分布

* Round-Robin：以轮询的方式把数据逐个放置在相邻节点上
* Range：按区间进行数据分布
* List：直接基于离散的各个取值做数据分布
* Hash：通过哈希函数把数据映射到不同节点上

starrocks支持range和hash 进行数据分布
分区是range方式，分桶是hash方式

即starrocks有两种数据分布
1. hash：不分区+分桶(不分区即一张表一个分区)
2. range+hash：分区+分桶


### 属性

```sql
CREATE TABLE
...
PROPERTIES (
    "replication_num" = "3",                -- 副本数，即每个tablet有几份，默认3
    "in_memory" = "false"                   -- 属性为 true 时，StarRocks 会尽可能将该表的数据和索引 Cache 到 BE 内存中，默认false
    "enable_persistent_index" = "false"     -- 持久化主键索引，同时使用磁盘和内存存储主键索引，默认false，通常情况下，持久化主键索引后，主键索引所占内存为之前的 1/10。
    "storage_format" = "DEFAULT",           -- 

    "storage_medium" = "SSD",               -- 当ENGINE 为 olap 时，可以设置初始存储介质(可选 SSD 和 HDD), 不设置此参数，初始存储介质由FE配置文件决定
    "storage_cooldown_time" = "yyyy-MM-dd HH:mm:ss",    -- 数据降冷时间(数据从SSD转移到HDD)，不设置此参数，不自动降冷


    "dynamic_partition.enable" = "true",    -- 是否开启动态分区，默认true
    "dynamic_partition.time_unit" = "DAY",  -- 动态分区粒度取值，(DAY、WEEK 或 MONTH) 时间粒度必须对应分区名后缀格式。具体对应规则如下：
                                                -- 取值为 DAY 时，分区名后缀的格式应该为 yyyyMMdd，例如 20200321。
                                                -- 取值为 WEEK 时，分区名后缀的格式应该为 yyyy_ww，例如 2020_13 代表 2020 年第 13 周。
                                                -- 取值为 MONTH 时，分区名后缀的格式应该为 yyyyMM，例如 202003。
    "dynamic_partition.start" = "-3",       -- 动态分区的开始时间，默认值为 -2147483648，最大-1，会删除此天数之前的分区
    "dynamic_partition.end" = "3",          -- 动态分区的结束时间，最小 1，会提前创建此天数之后的分区
    "dynamic_partition.prefix" = "p",       -- 动态分区名前缀 如 p20220909
    "dynamic_partition.buckets" = "32"      -- 动态分区的分桶数量，默认与 BUCKETS 关键词指定的分桶数量保持一致。
);
```







## 数据模型

* 数据模型(主键模型)
    * 明细模型 (Duplicate Key Model)
    * 聚合模型 (Aggregate Key Model)
    * 更新模型 (Unique Key Model)
    * 主键模型 (Primary Key Model)

* 主键特点：
    1. 主键通常为查询时过滤条件中频繁使用的维度列。
    2. 在明细模型中，主键可重复，不必满足唯一性约束
    3. 在聚合模型、主键模型和更新模型中，主键必须满足唯一性约束。
    4. 根据主键生成前缀索引 (Prefix Index) 。

* 主键注意：
    1. 建表语句中，主键必须定义在其他列之前
    2. 建表语句中，分区键和分桶键必须为主键
    3. 明细模型中，可以存在主键重复的数据行
    4. 聚合模型中，导入的数据中主键重复的数据行聚合为一行，即具有相同主键的指标列，会通过聚合函数进行聚合。
    5. 主键模型和更新模型中，最新导入的数据行，替换掉其他主键重复的数据行。这两种模型可以视为聚合模型的特殊情况，相当于在聚合模型中，为表的指标列指定聚合函数为 REPLACE
    6. 不为明细模型时，数据也会按照主键进行排序

### 明细模型

* 明细模型是默认的建表模型。明细模型中的主键也叫排序键
* 创建表时，支持定义主键(排序键)，可以通过 DUPLICATE KEY 显式定义，如果未指定，则默认选择表的前三列作为排序键。
* 导入时，支持追加新数据，不支持修改历史数据。
* 如果导入两行完全相同的数据，则明细模型会将这两行数据视为两行，而不是一行。

建表语句：指定 time 和 type 为排序键，id为分桶键
```sql
CREATE TABLE IF NOT EXISTS table_tmp (
    `time` DATETIME NOT NULL,
    `type` INT NOT NULL,
    `id` INT
    ...
)
DUPLICATE KEY(`time`, `type`)
DISTRIBUTED BY HASH(id) BUCKETS 8;
```

### 聚合模型


* 建表时，支持定义主键和指标列，并为指标列指定聚合函数。
* 当多条数据具有相同的主键时，指标列会进行聚合
* 主键可以通过 AGGREGATE KEY 显式定义。所有列必须为指标列或者主键，否则建表会失败。
* 如果不通过 AGGREGATE KEY 显示定义主键，则默认除指标列之外的列均为主键。
* 指标列需要使用的聚合函数指定


聚合的具体时机和机制如下：
1. 数据导入阶段：数据按批次导入至聚合模型时，每一个批次的数据形成一个版本，在一个版本中，同一主键的数据会进行一次聚合。
2. 后台文件合并阶段 (Compaction) ：多个版本的文件定期合并成一个大版本文件时，同一主键的数据会进行一次聚合。
3. 查询阶段：所有版本中同一主键的数据进行聚合，然后返回查询结果。


建表语句：将 site_id、date、city_code 作为主键，将 pv 作为指标列，并为指标列 pv 指定聚合函数为 SUM。
插入两条 site_id,date,city_code相同的数据时，会合并为一条，并将两条数据的pv值相加
```sql
-- 没有显示定义主键，则除指标列的其他均为主键
CREATE TABLE IF NOT EXISTS table_tmp (
    `site_id` LARGEINT NOT NULL,
    `date` DATE NOT NULL,
    `city_code` VARCHAR(20),
    `pv` BIGINT SUM DEFAULT "0"
)
DISTRIBUTED BY HASH(site_id) BUCKETS 8;
```


### 更新模型

* 通过 UNIQUE KEY 定义主键
* 同一主键保存多个版本，查询时返回主键相同的一组数据中的最新数据
* 采用了读时合并的策略。虽然写入时处理简单高效，但是查询时需要在线聚合多版本
<!-- * 导入数据时，仅支持全部更新，即导入任务需要指明所有列 -->

<!-- 
更新机制：
1. 可视为聚合模型的特殊情况，指标列指定的聚合函数为 REPLACE，返回具有相同主键的一组数据中的最新数据。
2. 数据分批次多次导入至更新模型，每一批次数据分配一个版本号，因此同一主键的数据可能有多个版本，查询时返回版本最新（即版本号最大）的数据
 -->

建表语句：create_time 和 order_id 为主键，order_id 为分桶键
```sql
CREATE TABLE IF NOT EXISTS orders (
    create_time DATE NOT NULL,
    order_id BIGINT NOT NULL,
    order_state INT,
    total_price BIGINT
)
UNIQUE KEY(create_time, order_id)
DISTRIBUTED BY HASH(order_id) BUCKETS 8;
```




### 主键模型

* 主键通过 PRIMARY KEY 定义。
* 采用了 Delete+Insert 的策略，保证同一个主键下仅存在一条记录
    * 更新操作时，通过主键索引找到该条记录的位置，并对其标记为删除，再插入一条新的记录 
    * 删除操作时，通过主键索引找到该条记录的位置，对其标记为删除
* 适用于事务型数据库的数据同步至 StarRocks


建表语句：指定dt 和 order_id 为主键
```sql
CREATE TABLE IF NOT EXISTS orders (
    dt date NOT NULL,
    order_id bigint NOT NULL,
    user_id int NOT NULL
) PRIMARY KEY (dt, order_id)
DISTRIBUTED BY HASH(order_id) BUCKETS 4
```