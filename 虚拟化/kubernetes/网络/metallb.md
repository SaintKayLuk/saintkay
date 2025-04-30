## metallb


查看各cni插件和 metalLB 的兼容性
```
https://metallb.universe.tf/installation/network-addons/
```





### 前提条件




如果您在 IPVS 模式下使用 kube-proxy，自 Kubernetes v1.14.2 起，您必须启用严格 ARP 模式。

建议搭配calico来使用，使用flannel无法访问，目前没找到原因


```sh
kubectl edit configmap -n kube-system kube-proxy
```

```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
  strictARP: true
```

---


### 安装metallb

和安装 calico 类似，采用了 CRD（Custom Resource Definitions）来配置


先创建个 memberllist 的 secret
```sh
# 先生成个秘钥
openssl rand -base64 128
```

再创建 Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: memberlist
  namespace: metallb-system
data:
  secretkey: <your_base64_encoded_secret>   # openssl rand -base64 128 的值
```



```sh
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
```



### 自定义资源配置

支持 Layer 2 和 BGP 两种模式

### Layer 2 模式

* MetalLB 使用 ARP（地址解析协议）或 NDP（邻居发现协议，针对 IPv6）来为外部流量分配 IP 地址，并在本地网络中宣布某个节点负责该 IP 地址。
* 外部设备（如路由器、交换机）可以将流量发送到该节点，节点再将流量路由到服务的后端 Pod。

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: my-ip-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.1.105-192.168.1.110     # 负载均衡ip
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement               # 使用l2模式
metadata:
  name: l2-advertisement
  namespace: metallb-system
spec: {}
```


### BGP 模式

* MetalLB 使用 BGP（边界网关协议）与网络中的路由器或交换机建立对等连接，并通过 BGP 向网络广告路由。这样，MetalLB 可以在网络中广播 Kubernetes 集群的 IP 地址，使得流量可以动态地分发到集群的多个节点。
* 适合企业级网络环境中有 BGP 路由器的情况。

---





### 其他


1. FRR 与 Calico 的结合
Calico BGP 模式：Calico 提供 BGP 路由的能力，使得每个 Kubernetes 节点都可以作为一个 BGP 对等体，与其他节点交换路由信息。Calico 可以与 FRR 一起工作，使用 FRR 作为 BGP 路由器来管理节点间和外部网络的路由。
FRR 的作用：通过 FRR，Kubernetes 节点可以作为 BGP 路由器，动态地宣布 Pod CIDR 和服务地址，从而无需手动配置路由表。FRR 可以在数据中心的网络设备中管理与集群的网络连接，使得跨节点、跨数据中心的网络更加高效。
1. FRR 与 MetalLB 的结合
MetalLB BGP 模式：MetalLB 是一种适用于裸金属集群的负载均衡器。当 MetalLB 以 BGP 模式 运行时，它可以通过与集群外部的路由器或交换机进行 BGP 会话，动态地向外部网络通告集群服务的 IP 地址。
FRR 的作用：MetalLB 可以使用 FRR 作为 BGP 对等体，将集群中的负载均衡 IP 地址（通常是服务的外部 IP 地址）通告给外部网络设备。这种模式下，FRR 可以与集群外的物理路由器交互，确保集群中的服务 IP 能够在集群外部被访问。


| 模式       | metallb-native.yaml                   | metallb-frr.yaml                                            |
| ---------- | ------------------------------------- | ----------------------------------------------------------- |
| 支持的协议 | Layer 2 (L2) 或 BGP                   | 主要是 BGP，但通过 FRR 提供高级路由功能                     |
| 复杂性     | 简单，适合中小型集群和简单 BGP 配置   | 复杂，适合大规模集群、跨数据中心，或需要复杂 BGP 路由的场景 |
| 使用场景   | 局域网或简单 BGP 配置，适合裸金属集群 | 大规模、企业级集群，复杂的路由环境，多层 BGP 网络拓扑       |
| 路由灵活性 | 基本 BGP 功能或 L2 通告，控制较少     | 更高级的 BGP 路由控制，支持复杂的网络拓扑和路由策略         |