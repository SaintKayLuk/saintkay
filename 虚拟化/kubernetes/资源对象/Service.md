## Service

Kubernetes 集群中的每个 Pod (即使是在同一个 Node 上的 Pod )都有一个惟一的 IP 地址，但是此ip只能集群内访问
Kubernetes 中的服务(Service)是一种抽象概念，它定义了 Pod 的逻辑集和访问 Pod 的协议

yaml示例

```yaml
apiVersion: v1                  #apiVersion版本
kind: Service                   #定义Service资源
metadata:                       
  name: my-service              #service名字
spec:
  type: ClusterIP               #service类型，默认ClusterIP，即不写时为ClusterIP，可选(ClusterIP/NodePort/ExternalName)
  clusterIP:                    #指定自己的集群 IP 地址,默认不写会自动分配，如果是 None，则创建Headless Service
  externalName: xxx.com         #type为ExternalName的时候指定映射的DNS名称

  sessionAffinity: ClientIP     #基于客户端的 IP 地址选择会话关联，默认为None
  sessionAffinityConfig:
    clientIP: 
      timeoutSeconds: 10800     #最大会话停留时间，默认10800秒(3小时)

  selector:
    app: v1.1                   #标签选择器，选择app=v1.1的标签的pod，会根据此标签自动创建endpoints，
  ports:            
    - name: http                #端口名，一个service多个端口时，必须每个端口指定名字
      protocol: TCP             #协议类型，默认TCP，可选(TCP,UDP,SCTP)   
      port: 80                  #service的port
      targetPort: 9376          #代理的pod的ip，为了方便起见，把port和targetPort设置一样
      nodePort: 30003           #可选参数，当type为NodePort时，手动设置NodePort端口，默认(30000-32767)取一个
    - name: https
      protocol: TCP
      port: 443
      targetPort: 9377

```

通过service访问pod流程，service会寻找和自己相同名字的endpoints，访问endpoints的pod列表ip中一个

```
Client --> Service --> endpoints --> Pod
```


Endpoints示例
```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: my-service
subsets:
  - addresses:
      - ip: 192.0.2.42          #自定义服务ip
    ports:
      - port: 9376              #服务端口   
```



type类型
* type: ClusterIP (默认)：只能从集群内访问
  * ClusterIP: None  创建无头服务(Headless Service)，此service不会分配 Cluster IP，kube-proxy 不会处理它们
* type: NodePort：每个选定的 Node 开放端口，使用 **NodeIP**:**NodePort**  访问，不选定node，则所有 NodeIP 都能访问
* type: LoadBalancer: 使用支持外部负载均衡器的云提供商的服务，本地集群可以安装metallb，[metallb](../网络/metallb.md)
  * 使用 LoadBalancer 的时候，其实也会开启一个nodeport的端口，可用来使用
* type: ExternalName：


有无标签选择器
* 有选择符(spec.selector)
  * 自动创建和service相同名字的 Endpoints 对象
* 没有选择符(spec.selector)
  * type为 ExternalName，查找其 CNAME 记录
  * type不是 ExternalName，查找与 Service 名称相同的任何 Endpoints 的记录





### 代理模式

* userspace ：v1.2之后被淘汰
* iptables  ：v1.2开始支持，并且v1.12之前的默认模式
* ipvs      ：v1.8开始支持（lvs的内核态）

#### userspace代理模式(用户空间模式)

```
kubu-proxy --> 监控 --> Service 和 Endpoints 的添加和移除
    ↓
配置 iptables 规则
    ↓
clusterIP:port  <---- Client
    ↓
    ↓
代理到本地随机端口 --> pod
```

1. 默认策略，轮询选择pod
2. 第一个pod 没有响应，会自动使用其他 Pod 重试


#### iptables代理模式
```
kubu-proxy --> 监控 --> Service 和 Endpoints 的添加和移除
    ↓
配置 iptables 规则
    ↓
clusterIP:port  <---- Client
    ↓
   pod
```
1. 默认策略，随机选择一个后端。
2. 如果 kube-proxy 所选的第一个 Pod 没有响应， 则连接失败
3. 使用 Pod 就绪探测器，以便 iptables 模式下的 kube-proxy 仅看到测试正常的后端


#### ipvs代理模式
```
kubu-proxy --> 监控 --> Service 和 Endpoints
    ↓
调用 netlink 接口创建 IPVS 规则

```


1. 启动 kube-proxy 前确保 IPVS 在节点上可用
2. kube-proxy 以 IPVS 代理模式启动时，如果未检测到 IPVS 内核模块，则以 iptables 代理模式运行
3. 负载均衡模式
   * rr：轮替（Round-Robin）
   * lc：最少链接（Least Connection），即打开链接数量最少者优先
   * dh：目标地址哈希（Destination Hashing）
   * sh：源地址哈希（Source Hashing）
   * sed：最短预期延迟（Shortest Expected Delay）
   * nq：从不排队（Never Queue）





