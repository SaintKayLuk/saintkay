
### osd


```sh
#启动一个服务，添加所有可用设备到ceph，后期添加新硬盘也会自动添加
ceph orch apply osd --all-available-devices
#取消自动添加
ceph orch apply osd --all-available-devices --unmanaged=true

#添加指定磁盘，手动添加后 会显示为 osd.None 而此service无法被删除，会提示找不到name
ceph orch daemon add osd <host>:<device-path>
#例：添加 ceph-1 主机的 /dev/sdb
ceph orch daemon add osd ceph-1:/dev/sdb
```

删除osd
```sh
#删除 CRUSH 图的对应 OSD 条目
ceph osd crush remove osd.0
#删除 OSD 认证密钥：
ceph auth del osd.0
#删除osd
ceph osd rm 0
```


```sh
#查看pool
ceph osd pool ls

#删除pool，要先设置mon的配置 mon_allow_pool_delete = true
#输入 2 遍pool
ceph osd pool rm <pool_name> <pool_name> --yes-i-really-really-mean-it

#查看pool的pg
ceph pg ls-by-pool device_health_metrics





#查看crush的rule
ceph osd crush rule ls
#查看名为 device_health_metrics 的 pool 使用的crush规则
ceph osd pool get device_health_metrics crush_rule
#创建一个replicated_rule_osd的规则
ceph osd crush rule create-replicated replicated_rule_osd default osd
#
ceph osd crush rule dump replicated_rule_osd
#把 replicated_rule_osd 规则分配给名为 device_health_metrics 的 pool
ceph osd pool set device_health_metrics crush_rule replicated_rule_osd
```


```sh
#size是pool的副本
#min_size是表示至少还有几个副本存活可提供io服务
#szie和min_size 的默认值分别是 3 和 2
ceph osd pool set <pool-name>  size 1
ceph osd pool set <pool-name>  min_size 1

ceph osd pool get <pool-name>  size
```


