MESOS  APACHE  分布式资源管理框架   2019-5  Twitter  》 Kubernetes

Docker Swarm  2019-07   阿里云宣布  Docker Swarm  剔除

Kubernetes  Google    10年容器化基础架构  borg   GO 语言   Borg 
	特点：
		轻量级：消耗资源小
		开源
		弹性伸缩
		负载均衡：IPVS
		
适合人群：软件工程师 测试工程师  运维工程师 软件架构师  项目经理


介绍说明：  前世今生   KUbernetes 框架  KUbernetes关键字含义

基础概念： 什么是 Pod   控制器类型  K8S 网络通讯模式 

Kubernetes：  构建 K8S 集群

资源清单：资源   掌握资源清单的语法   编写 Pod   掌握 Pod 的生命周期***

Pod 控制器：掌握各种控制器的特点以及使用定义方式

服务发现：掌握 SVC 原理及其构建方式

存储：掌握多种存储类型的特点 并且能够在不同环境中选择合适的存储方案（有自己的简介）

调度器：掌握调度器原理   能够根据要求把Pod 定义到想要的节点运行

安全：集群的认证  鉴权   访问控制 原理及其流程 

HELM：Linux yum    掌握 HELM 原理   HELM 模板自定义  HELM 部署一些常用插件

运维：修改Kubeadm 达到证书可用期限为 10年     能够构建高可用的 Kubernetes 集群



服务分类
	有状态服务：DBMS  
	无状态服务：LVS APACHE
	
高可用集群副本数据最好是 >= 3 奇数个
	
	
APISERVER：所有服务访问统一入口
CrontrollerManager：维持副本期望数目
Scheduler：：负责介绍任务，选择合适的节点进行分配任务
ETCD：键值对数据库  储存K8S集群所有重要信息（持久化）
Kubelet：直接跟容器引擎交互实现容器的生命周期管理
Kube-proxy：负责写入规则至 IPTABLES、IPVS 实现服务映射访问的
COREDNS：可以为集群中的SVC创建一个域名IP的对应关系解析
DASHBOARD：给 K8S 集群提供一个 B/S 结构访问体系
INGRESS CONTROLLER：官方只能实现四层代理，INGRESS 可以实现七层代理
FEDERATION：提供一个可以跨集群中心多K8S统一管理功能
PROMETHEUS：提供K8S集群的监控能力
ELK：提供 K8S 集群日志统一分析介入平台
	
	
	
### Pod
自主式pod
控制器管理的pod

pod内容器共享网络栈，存储卷，

控制器类型
* replicationcontroller 期望副本数，
* replicaset 和replicationcontroller没有本质区别，支持集合式selector
* deployment ，自动管理replicaset
* HPA 仅适用于rs和deployment
* statefulset 为解决有状态服务
  * 稳定持久化存储，基于PVC实现
  * 稳定网络标志，基于Headless service，即没有cluster ID 的 service
  * 有序部署
  * 有序收缩
* daemonset 确保全部或者一些node上运行一个pod的副本 
* job 负责批处理任务，仅执行一次，保证批处理任务的一个或多个pod成功结束
* cron job 管理基于时间的job
  * 在给定时间点只执行一次
  * 周期性地在给定时间点执行
	
 
网络模式

同一个pod内多个容器之间 lo，共享一个网络命名空间，共享同一个Linux协议栈
各pod之间的通讯 overlay network
pod 与 service 之间通讯 各节点的iptables规则



