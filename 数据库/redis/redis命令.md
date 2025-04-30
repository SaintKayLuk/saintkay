## 支持的数据格式

redis数据基本格式为 key-value，不同的是value的数据类型，例如hash的value就是一对对的键值对

* string(字符串)
* hash(哈希)
* list(列表)
* set(集合)
* zset(sorted set:有序集合)


操作redis一般返回值为数字，返回是否的命令，1代表是，0代表否，
修改或插入多个元素的情况下，返回数字几代表成功了几个

## key命令

| 命令               | 作用                                        |
|--------------------|-------------------------------------------|
| DEL key            | 删除某个key                                 |
| EXISTS key         | 判断某个key是否存在，存在返回1，不存在返回0   |
| EXPIRE key seconds | 设置某个key的过期时间，以秒为单位，几秒后过期 |
| KEYS pattern       | 根据条件查找key，例如查找所有key KEYS *      |
| TYPE key           | 返回 key 所储存的值的类型                   |

## string

格式：key value

键值对，一个key对应一个value，string 类型的值最大能存储 512MB

| 命令          | 作用            |
|---------------|---------------|
| SET key value | 设置一个key的值 |
| GET key       | 获取key的值     |

## hash

格式：key field value [field value ...]

键值对的集合，每个 hash 可以存储 2的32次-1个键值对

| 命令                                   | 作用                                         |
|----------------------------------------|----------------------------------------------|
| HSET key field1 value1 [field2 value2 ...] |                                              |
| HGET key field                         | 获取指定hash表中某个字段的值                 |
| HMGET key field1 [field2 ...]          | 获取指定hash表中一个或者多个字段的值         |
| HKEYS key                              | 获取指定hash表中所有的字段                   |
| HGETALL key                            | 获取指定hash表中所有的字段和值               |
| HDEL key field1 [field2 ...]           | 删除一个或多个hash表字段                     |
| HEXISTS key field                      | 判断指定的字段是否存在，存在返回1，不存在返回0 |

## list

格式：key value [value ...]

简单的字符串列表，按照插入顺序排序,每个列表最多可存储 2的32次-1个值 

| 命令                          | 作用                                  |
|-------------------------------|-------------------------------------|
| LPUSH key value1 [value2 ...] | 从列表左边开始插入数据，最开始处插入   |
| RPUSH key value1 [value2 ...] | 从列表最右边开始插入数据，最后位置插入 |
| LINDEX key index              | 通过索引获取列表中的元素              |
| LLEN key                      | 获取列表长度                          |

```
例如，通过lpush插入数据，最新插入的数据在最左边，即index为0 
127.0.0.1:6379> LPUSH test aa bb cc
3
127.0.0.1:6379> LINDEX test 0
cc
```
## set

格式：key value [value ...]

string类型的无序集合，通过哈希表实现的，没有重复值

| 命令                         | 作用                         |
|------------------------------|----------------------------|
| SADD key value1 [value2 ...] | 向集合中添加一个或多个值     |
| SCARD key                    | 获取集合中元素个数           |
| SISMEMBER key member         | 判断集合中是否存在menber元素 |
| SMEMBERS key                 | 返回集合中所有成员           |

## zset

格式：key socre member [score member ...]

string类型的有序集合，和set一样，没有重复值，
score可以一样，但是member不能一样，即可以存在score一样但member不一样的值

| 命令                                         | 作用                                                  |
|----------------------------------------------|-----------------------------------------------------|
| ZADD key score1 member1 [score2 member2 ...] | 向有序集合添加一个或多个成员，或者更新已存在成员的分数 |
| ZCARD key                                    | 获取有序集合的成员数                                  |


