## always on

sql server 的高可用，依赖于 AD，需要sql server 服务器加入域，并且依赖于 故障转移集群工具











#### 设置读写分离，主副本读写，辅助副本只读




需要先设置只读地址，虽然连的是 ag 的地址，但是只读连接需要存在
```sql
-- 设置只读地址
ALTER AVAILABILITY GROUP alwayson 
MODIFY REPLICA ON N'U9C-DB1' 
WITH (
    SECONDARY_ROLE (
        READ_ONLY_ROUTING_URL = N'TCP://U9C-DB1.U9C.COM:1433'
    )
);

-- 设置只读地址
ALTER AVAILABILITY GROUP alwayson 
MODIFY REPLICA ON N'U9C-DB2' 
WITH (
    SECONDARY_ROLE (
        READ_ONLY_ROUTING_URL = N'TCP://U9C-DB2.U9C.COM:1433'
    )
);

```


```sql
-- 当主库是 U9C-DB1 时，读请求依次尝试 U9C-DB2 → U9C-DB1
ALTER AVAILABILITY GROUP alwayson 
MODIFY REPLICA ON N'U9C-DB1' 
WITH (
    PRIMARY_ROLE (
        READ_ONLY_ROUTING_LIST = ('U9C-DB2','U9C-DB1')   
    )
);

-- 当主库是 U9C-DB2 时，读请求依次尝试 U9C-DB1 → U9C-DB2
ALTER AVAILABILITY GROUP alwayson 
MODIFY REPLICA ON N'U9C-DB2' 
WITH (
    PRIMARY_ROLE (
        READ_ONLY_ROUTING_LIST = ('U9C-DB1','U9C-DB2')   
    )
);



```







