## rgw


创建rgw守护进程
```sh
ceph orch apply rgw <realm_name> <zone_name> 
```


一个realm由多个zone组成，一个zone由多个ceph gateway实例组成
一个zonegroup由多个zone组成，用于一个group内不同zone复制
```
        /   zone
                    /   rgw实例
realm  |    zone   |    rgw实例
                    \   rgw实例
        \   zone

```



<!-- 一个realm下有一个或者多个zone，可以不需要zonegroup -->


<!-- radosgw-admin period update --commit -->
<!-- radosgw-admin period update --commit -->
<!-- radosgw-admin period update --commit -->
<!-- radosgw-admin period update --commit -->
<!-- radosgw-admin period update --commit -->
## 创建过程

1. 创建realm
2. 创建zonegroup，指定realm
3. 创建zone，指定zonegroup


### realm

```sh
#创建realm
radosgw-admin realm
    list        # 查看 realm 列表
    create --rgw-realm=<realm_name>     #创建realm
        --default                           #创建realm的时候指定为默认

    default --rgw-realm=<realm_name>    #设置某个realm为默认，设置为默认之后，不指定 --rgw-realm=<realm_name> 则就是操作默认的realm，除非指定realm
    delete --rgw-realm=<realm_name>     #删除某个realm
    

#例：创建一个名为 hangzhou 的realm，并且设置为默认
radosgw-admin realm create --rgw-realm=hangzhou --default   
```


### zonegroup

一个zonegroup下的zone可以实现跨地域、集群 复制
一个zonegruop下可以有多个zone，zone也可以没有zonegroup

```sh
radosgw-admin zonegroup 
    create --rgw-zonegroup=<zonegroup_name>     #创建一个zonegroup 
        --rgw-realm=<name>  #指定realm，如果不指定，则为默认的realm
        --master            #指定为master
        --default           #指定为默认group
    
    default --rgw-zonegroup=<zonegroup_name>    #设置一个zonegroup为默认
    delete --rgw-zonegroup=<zonegroup_name>     #删除一个zonegroup

    add --rgw-zonegroup=<zonegroup_name> --rgw-zone=<zone_name> # 将一个zone加入到zonegroup中
    
```

例：创建一个zonegroup
```
radosgw-admin zonegroup create --rgw-zonegroup=group1 --rgw-realm=hangzhou --master --default   
```

### zone


```sh
radosgw-admin zone 
    create --rgw-zone=<zone_name>       #创建一个zone
        --zonegroup=<zonegroup-name>        #指定zonegroup
        --master                            #指定是masterzone
        --default                           #指定default
```

例：
```
radosgw-admin zone create --rgw-zonegroup=group1 --rgw-zone=A --master --default
```

```
#删除zone
radosgw-admin zone delete --rgw-zone=<zone_name>
#删除zonegroup
radosgw-admin zonegroup delete --rgw-zonegroup=<zonegroup_name>
```


### xxx

```sh
#添加rgw用户， --system 为系统用户
radosgw-admin user create --uid=<user_id> --display-name=<display_name> --system
#查看用户信息
radosgw-admin user info --uid=<user_id>


#添加dashboard的用户
ceph dashboard set-rgw-api-user-id <user_id>
#添加 access-key 和 secret-key
ceph dashboard set-rgw-api-access-key <access-key>
ceph dashboard set-rgw-api-secret-key <secret-key>

#根本不同版本，把key写到文件里
echo <access-key> > access.key
echo <secret-key> > secret.key
ceph dashboard set-rgw-api-access-key -i access.key 
ceph dashboard set-rgw-api-secret-key -i secret.key



ceph dashboard set-rgw-api-ssl-verify False
ceph dashboard get-rgw-api-scheme http

#例：添加一个控制页的用户
radosgw-admin user create --uid=dashboard --display-name=dashboard --system

```



#### 修改端口


默认是80端口

进入rgw的容器 

在 /etc/ceph/ceph.conf 文件中 加入以下一行，修改端口为7480

rgw_frontends = beast port=7480
