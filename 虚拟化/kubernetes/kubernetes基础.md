## kubernetes组件

#### 控制平面组件（Control Plane Components）

* kube-apiserver
* etcd：存储kubernetes集群数据
* kube-scheduler：调度pod
* kube-controller-manager
  + 节点控制器（Node Controller）: 负责在节点出现故障时进行通知和响应
  + 任务控制器（Job controller）: 监测代表一次性任务的 Job 对象，然后创建 Pods 来运行这些任务直至完成
  + 端点控制器（Endpoints Controller）: 填充端点(Endpoints)对象(即加入 Service 与 Pod)
  + 服务帐户和令牌控制器（Service Account & Token Controllers）: 为新的命名空间创建默认帐户和 API 访问令牌
* cloud-controller-manager

#### node组件

* kubelet：每个节点（node）上运行的代理。 它保证容器（containers）都 运行在 Pod 中。
* kube-proxy：每个节点上运行的网络代理， 实现 Kubernetes 服务（Service） 概念的一部分。
* Container Runtime（容器运行时）
  + docker
  + containerd

#### 插件（Addons）

* CoreDNS：是一种灵活的，可扩展的 DNS 服务器，可以 安装为集群内的 Pod 提供 DNS 服务
* Dashboard：是Kubernetes 集群的通用的、基于 Web 的用户界面
* Prometheus：可以原生监控 Kubernetes、 节点和 Prometheus 本身
* 日志

## node节点

* 地址
* 状况
* 容量与可分配
* 信息

```sh
#查看节点详细信息
kubectl describe node <节点名称>
```

### 地址

Addresses 字段描述地址

* HostName：由节点的内核设置。可以通过 kubelet 的 --hostname-override 参数覆盖。
* ExternalIP：通常是节点的可外部路由（从集群外可访问）的 IP 地址。
* InternalIP：通常是节点的仅可在集群内部路由的 IP 地址。

### 状况

conditions 字段描述状态

| 节点状况           | 描述                                                                                                                                      |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Ready              | 如节点是健康的并已经准备好接收 Pod 则为 True；False 表示节点不健康而且不能接收 Pod；Unknown 表示节点控制器在最近node-monitor-grace-period | 期间（默认 40 秒）没有收到节点的消息 |
| DiskPressure       | True 表示节点的空闲空间不足以用于添加新 Pod, 否则为 False                                                                                 |
| MemoryPressure     | True 表示节点存在内存压力，即节点内存可用量低，否则为 False                                                                               |
| PIDPressure        | True 表示节点存在进程压力，即节点上进程过多；否则为 False                                                                                 |
| NetworkUnavailable | True 表示节点网络配置不正确；否则为 False                                                                                                 |

### 容量与可分配

Capacity 字段描述字段总量
Allocatable 字段描述可供给普通pod消耗的容量

### 信息

System Info 字段描述系统信息，kubelet，kube-proxy版本等












