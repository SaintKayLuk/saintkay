## mysql to clickhouse

```
mysql ----> 分析库
        ↓
mysql ----> clickhouse
```

1. mysql 同步到 clickhouse
   1. mysql新增 --> clickhouse新增
   2. mysql修改 --> clickhouse新增(updateTime为插入时间)
   3. mysql删除 --> clickhouse新增(isDelete=1) 
2. 每张表多两个字段
   1. isDelete：删除标记，默认为0，为1则此记录被删除
   2. updateTime：每条记录插入时间

## 查询SQL

因为有多条记录，查询id相同的记录时，取updateTime最大的一条记录，再排除isDelete=1的记录

例：查询 user_custom 用户 id,phone
```sql
SELECT
   argMax(id,updateTime),
   argMax(phone,updateTime),
   argMax(isDelete,updateTime) isdel
FROM `atlantis-cloud-mage`.`user_custom`
WHERE antiFraudCodeStatus  = 'green' GROUP BY id HAVING isdel = 0
```



使用聚合函数等，把上述sql作为子查询

例：查询 user_custom 的绿码用户总数
```sql
SELECT COUNT(*) from(
	SELECT
	   argMax(id,updateTime),
	   argMax(isDelete,updateTime) isdel
	FROM `atlantis-cloud-mage`.`user_custom`
	WHERE antiFraudCodeStatus  = 'green' GROUP BY id HAVING isdel = 0
)
```

例：查询今日和昨日拦截数
```sql
SELECT * FROM (
   select sum (todayCount) from (
      SELECT  argMax (count,updateTime) todayCount,argMax (isDelete,updateTime) isdel 
      FROM `atlantis-cloud-mage-warehouse`.url_intercept_day_address 
      WHERE cityId  = 210874 AND `day` = 20220531 group by id HAVING isdel=0
	)
)t2
LEFT JOIN (
   select sum (yesterdayCount) from (
      SELECT argMax(count,updateTime) yesterdayCount ,argMax (isDelete,updateTime) isdel
      FROM `atlantis-cloud-mage-warehouse`.url_intercept_day_address 
      WHERE cityId = 210874 AND `day`  = 20220530 group by id  HAVING isdel =0
   )
)t3 on 1=1
```

