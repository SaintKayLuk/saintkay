

# 基本组件

三个核心组件，必不可少
* ceph-mon：集群监视器，通常需要3个来实现高可用
* ceph-mgr：集群管理器
* ceph-osd：对象存储守护程序，存储数据，处理数据复制，恢复，再平衡 通常需要3个来实现高可用


其他组件
* ceph-mds：Ceph文件系统存储元数据，块存储和对象存储不需要使用cpeh-mds
* cephadm：集群管理工具，相当于于kubeadm




osd是一个物理存储设备，例如一块硬盘，或者多块硬盘组合成的一个osd
pg是对象存储集合，即相同存储策略的存储集合
pool是逻辑存储资源池

一个pg可以在不同ods上，一个osd可以包含多个pg
一个pool由多个pg组成

osd的状态
* in：在集群内
* out：在集群外
* up：存活
* down：下线

正常状态应该是 in + up


# 支持3种存储

* 块存储
* 对象存储
* 文件存储


# ceph系统层次结构

一共分为四层

1. 最底层为 **RADOS**，由几个组件组合而成
   1. OSB(Object Storage Device)
   2. Monitor
   3. 
2. 基础库 LIBRADOS，用于调用底层RADOS
3. 应用接口层
   * CephFS：文件存储接口
   * RBD(Ceph Block Devices)：块存储接口
   * RGW(Ceph Object Storage Gateway)：对象存储接口
4. 应用层


## ceph文件存储

客户端挂载方式
* 使用内核挂载，至少需要4.x以上内核
* 使用fuse挂载，挂载在用户空间，性能略差，







在外面启动，启动mon和mgr组件要使用cephadm，集群都没起来，进去执行命令也执行不了
cephadm run --name xxx --fsid xxx

cephadm shell进去之后，启动其他进程，例如osd，rgw等进集群内部
启动进程
ceph orch daemon start osd.0

