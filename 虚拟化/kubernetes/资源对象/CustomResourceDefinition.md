# CRD


在 Kubernetes 中，CRD (Custom Resource Definition) 是一种扩展 Kubernetes API 的机制，允许用户定义自定义资源（Custom Resources，简称 CR）。这使得 Kubernetes 不仅可以管理自身的核心资源（如 Pods、Services、Deployments 等），还可以支持和管理自定义的资源类型。

1. CRD 的概念
CRD 是 Kubernetes 内置的一种功能，允许你定义一种新的资源类型，使得 Kubernetes API 可以识别和管理这些自定义资源。通过 CRD，用户可以像操作原生资源一样管理自定义资源。

例如，安装 Calico 或 MetalLB 时，这些网络插件或服务会定义和注册一组新的 CRD，用户通过这些 CRD 来配置网络策略、IP 地址池等。

核心资源：Kubernetes 原生支持的资源类型，比如 Pod、Service、ConfigMap 等。
自定义资源：通过 CRD 定义的资源类型，比如 Calico 的 NetworkPolicy 或 MetalLB 的 IPAddressPool。
2. CRD 在 Kubernetes 中的作用
CRD 允许开发者创建全新的 API 扩展，并让 Kubernetes 通过这些扩展执行自定义逻辑。许多 Kubernetes 插件、运维工具都是通过 CRD 来实现的。以下是一些 CRD 的具体应用：

Calico：定义了网络策略、IPAM（IP地址管理）等 CRD，用来管理集群的网络配置。例如 NetworkPolicy 用来定义网络访问控制规则。

NetworkPolicy：定义 pod 之间或者 pod 与外部服务之间的通信规则。
IPPool：定义了可分配的 IP 地址范围。
MetalLB：使用 CRD 来定义 IP 地址池和负载均衡配置。

IPAddressPool：用于定义 MetalLB 在 L2 模式下分配 IP 地址的范围。
BGPPeer：在 BGP 模式下，定义 BGP 对等体的配置。
Ingress Controllers：比如 ingress-nginx，也可以通过 CRD 扩展，定义自定义的 Ingress 规则。

3. CRD 的作用过程
当你安装一个依赖于 CRD 的应用时，它通常会做以下几步：

创建 CRD：这些应用首先创建自定义资源定义（CRD），例如：

metallb.io/v1beta1 下的 IPAddressPool
projectcalico.org/v1 下的 NetworkPolicy
这些定义告诉 Kubernetes，这些新的 API 类型现在可以使用。

操作自定义资源：安装完成后，你可以创建、更新、删除这些自定义资源。Kubernetes API 现在识别这些资源，并根据它们的定义来管理其生命周期。例如：

通过 kubectl apply -f 创建一个 IPAddressPool 来指定负载均衡的 IP 地址范围。
通过 kubectl apply -f 创建 NetworkPolicy 来控制网络流量。
控制器处理自定义资源：每个 CRD 通常有对应的控制器来处理资源的变化，控制器会监视这些自定义资源的状态，并执行相应的逻辑。例如：

当创建一个新的 IPAddressPool 时，MetalLB 的控制器会根据定义的 IP 地址范围来分配外部 IP 地址。
当定义一个 NetworkPolicy 时，Calico 的控制器会确保网络策略被正确应用。
4. CRD 的文件格式
一个 CRD 文件通常包含自定义 API 的版本、种类及其定义的字段结构。例如，下面是一个简单的 CRD 定义：


```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: ipaddresspools.metallb.io
spec:
  group: metallb.io
  versions:
    - name: v1beta1
      served: true
      storage: true
  scope: Namespaced
  names:
    plural: ipaddresspools
    singular: ipaddresspool
    kind: IPAddressPool
    shortNames:
      - ippool
```
这个定义告诉 Kubernetes 新的 IPAddressPool 类型的资源应该如何识别和操作。

1. CRD 的使用场景
CRD 被广泛用于 Kubernetes 插件和运维工具中，如下：

网络管理：如 Calico、Cilium 等网络插件使用 CRD 来管理网络策略、IP 地址等资源。
存储管理：像 Rook 和 Ceph 等分布式存储系统使用 CRD 来定义存储池和卷。
负载均衡：MetalLB 使用 CRD 来定义 IP 地址池和负载均衡器的配置。
总结
CRD 是 Kubernetes 中扩展 API 的方式，用于定义和管理自定义资源。
通过 CRD，你可以为 Kubernetes 添加全新的功能，插件和工具（如 Calico 和 MetalLB）使用 CRD 来定义和管理复杂的资源。
使用 CRD 可以让 Kubernetes 不仅限于管理核心资源，还能够灵活适应各种插件和业务场景。