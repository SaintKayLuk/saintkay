# kubeadm


初始化一个集群
```sh
kubeadm init [选项]
    --apiserver-advertise-address xxx   #API服务器监听的 IP 地址，就是自己这个控制平面节点的ip
    --control-plane-endpoint xxx        #所有控制平面节点设置共享端点。 负载均衡器的 DNS 名称或 IP 地址      
    --apiserver-bind-port xxx           #API服务器绑定的端口，默认6443
    --cert-dir xxx                      #保存和存储证书的路径。默认值："/etc/kubernetes/pki"
    --config xxx                        #kubeadm 配置文件的路径。
    --image-repository xxx              #拉取kubernetes镜像的容器仓库，默认值："k8s.gcr.io"
    --kubernetes-version xx             #指定kubernetes版本，默认值："stable-1"
    --pod-network-cidr xx.xx.xx.xx/xx   #pod的ip段。如果设置了这个参数，将会为每一个节点自动分配 CIDRs
    --service-cidr xx.xx.xx.xx/xx       #service的ip段， 默认值："10.96.0.0/12"
    --cri-socket xxx                    #CRI 套接字的路径，不写自动寻找，如果存在多个则可以用此参数指定
    --dry-run                           #不做任何更改；只输出将要执行的操作，可以用来研究kubeadm init的操作流程
    --ignore-preflight-errors=xx,xx     #忽略检查时候的错误列表；例如：取值为 'all' 时将忽略检查中的所有错误。
```


## 初始化控制平面节点

创建一个单控制面板的节点
```sh
kubeadm init --apiserver-advertise-address xx.xx.xx.xx --image-repository registry.aliyuncs.com/google_containers --kubernetes-version v1.25.14 --pod-network-cidr 10.10.0.0/16 --service-cidr 10.20.0.0/16
```

## 初始话高可用控制节点
如果初始化一个高可用集群，控制节点大于等于3个以上的时候，需要 --control-plane-endpoint 参数，指向负载均衡地址或者dns地址，

**可以使用云厂商的DNS解析，解析3同一个域名3条记录到本地3个ip**

```sh
#第一个控制节点，api.k8s.saintkay.com 是DNS地址，指向 192.160.0.101 和 192.160.0.102
kubeadm init --control-plane-endpoint api.k8s.saintkay.com --upload-certs
```

--control-plane-endpoint 和 --upload-certs 都需要

其他控制面板节点加入，
```sh
kubeadm join api.k8s.saintkay.com --token xxx --discovery-token-ca-cert-hash xxx --control-plane --certificate-key xxx
```

kubeadm-certs Secret 和解密密钥会在两个小时后失效，其他控制节点加入需要，则在已经是 控制面板节点上运行此命令
```sh
kubeadm init phase upload-certs --upload-certs
```

## init 工作流程（学习使用）



kubeadm init 整个流程，可以通过 kubeadm init --help 来查看，kubeadm init 的整个流程就按照这个来执行
```
preflight                    Run pre-flight checks
certs                        Certificate generation
  /ca                          Generate the self-signed Kubernetes CA to provision identities for other Kubernetes components
  /apiserver                   Generate the certificate for serving the Kubernetes API
  /apiserver-kubelet-client    Generate the certificate for the API server to connect to kubelet
  /front-proxy-ca              Generate the self-signed CA to provision identities for front proxy
  /front-proxy-client          Generate the certificate for the front proxy client
  /etcd-ca                     Generate the self-signed CA to provision identities for etcd
  /etcd-server                 Generate the certificate for serving etcd
  /etcd-peer                   Generate the certificate for etcd nodes to communicate with each other
  /etcd-healthcheck-client     Generate the certificate for liveness probes to healthcheck etcd
  /apiserver-etcd-client       Generate the certificate the apiserver uses to access etcd
  /sa                          Generate a private key for signing service account tokens along with its public key
kubeconfig                   Generate all kubeconfig files necessary to establish the control plane and the admin kubeconfig file
  /admin                       Generate a kubeconfig file for the admin to use and for kubeadm itself
  /kubelet                     Generate a kubeconfig file for the kubelet to use *only* for cluster bootstrapping purposes
  /controller-manager          Generate a kubeconfig file for the controller manager to use
  /scheduler                   Generate a kubeconfig file for the scheduler to use
kubelet-start                Write kubelet settings and (re)start the kubelet
control-plane                Generate all static Pod manifest files necessary to establish the control plane
  /apiserver                   Generates the kube-apiserver static Pod manifest
  /controller-manager          Generates the kube-controller-manager static Pod manifest
  /scheduler                   Generates the kube-scheduler static Pod manifest
etcd                         Generate static Pod manifest file for local etcd
  /local                       Generate the static Pod manifest file for a local, single-node local etcd instance
upload-config                Upload the kubeadm and kubelet configuration to a ConfigMap
  /kubeadm                     Upload the kubeadm ClusterConfiguration to a ConfigMap
  /kubelet                     Upload the kubelet component config to a ConfigMap
upload-certs                 Upload certificates to kubeadm-certs
mark-control-plane           Mark a node as a control-plane
bootstrap-token              Generates bootstrap tokens used to join a node to a cluster
kubelet-finalize             Updates settings relevant to the kubelet after TLS bootstrap
  /experimental-cert-rotation  Enable kubelet client certificate rotation
addon                        Install required addons for passing Conformance tests
  /coredns                     Install the CoreDNS addon to a Kubernetes cluster
  /kube-proxy                  Install the kube-proxy addon to a Kubernetes cluster
show-join-command            Show the join command for control-plane and worker node
```

可以通过 kubeadm init phase 一个个执行，例如
```sh
kubeadm init phase preflight
```

可以通过 --help 命令来查看特定父阶段的子阶段列表
```sh
kubeadm init phase control-plane --help
```

也可以查看子阶段的可用选项
```sh
kubeadm init phase control-plane controller-manager --help
```

使用 --skip-phases 跳过某些阶段
```sh
sudo kubeadm init phase control-plane all --config=configfile.yaml
sudo kubeadm init phase etcd local --config=configfile.yaml
# 你现在可以修改控制平面和 etcd 清单文件
sudo kubeadm init --skip-phases=control-plane,etcd --config=configfile.yaml
```



### 1、预检查

#### 详细输出

加 --v=5 可输出详细信息
```sh
kubeadm init phase preflight  --v=5
```

#### 忽略错误
在做出变更前运行一系列的预检项来验证系统状态，可以通过 --ignore-preflight-errors 参数跳过错误检查

忽略所有错误
```sh
kubeadm init phase preflight --ignore-preflight-errors=all
```

常见的错误
```
Swap                                                        检查交换分区是否禁用。
SystemVerification                                          系统验证检查。
IsPrivilegedUser                                            检查否以特权用户（通常是 root 用户）运行 kubeadm 命令
FileContent--proc-sys-net-bridge-bridge-nf-call-iptables    检查内核参数设置。
FileContent--proc-sys-net-ipv4-ip_forward                   检查 IP 转发设置。
```

例：忽略多个错误
```sh
kubeadm init phase --ignore-preflight-errors=Swap,IsPrivilegedUser
```

#### 提前下载镜像

虽然镜像不是在 preflight 阶段下载的，但是会尝试，但由于 preflight不能指定镜像版本，所以我们可以提前下好
```sh
# 查看需要的镜像
kubeadm config images list

# 下载镜像
kubeadm config images pull --image-repository registry.aliyuncs.com/google_containers --kubernetes-version v1.25.14
```


### 2、生成证书
生成一个自签名的 CA 证书来为集群中的每一个组件建立身份标识。可以将自己的证书放到证书目录中（默认为 /etc/kubernetes/pki） 来提供自己的 CA 证书以及/或者密钥，证书目录可以通过 --cert-dir 设置


```
kubeadm init phase certs

Available Commands:
  all                      Generate all certificates
  apiserver                Generate the certificate for serving the Kubernetes API
  apiserver-etcd-client    Generate the certificate the apiserver uses to access etcd
  apiserver-kubelet-client Generate the certificate for the API server to connect to kubelet
  ca                       Generate the self-signed Kubernetes CA to provision identities for other Kubernetes components
  etcd-ca                  Generate the self-signed CA to provision identities for etcd
  etcd-healthcheck-client  Generate the certificate for liveness probes to healthcheck etcd
  etcd-peer                Generate the certificate for etcd nodes to communicate with each other
  etcd-server              Generate the certificate for serving etcd
  front-proxy-ca           Generate the self-signed CA to provision identities for front proxy
  front-proxy-client       Generate the certificate for the front proxy client
  sa                       Generate a private key for signing service account tokens along with its public key
```

生成所有证书
```sh
kubeadm init phase certs all
```

证书路径保存默认保存在
```
/etc/kubernetes/pki
```


### 3、生成配置文件
将 kubeconfig 文件写入 /etc/kubernetes/ 目录以便 kubelet、控制器管理器和调度器用来连接到 API 服务器，它们每一个都有自己的身份标识，
同时生成一个名为 admin.conf 的独立的 kubeconfig 文件，用于管理操作。


生成配置文件，可以单独生成，也可以用all全部生成
```sh
kubeadm init phase kubeconfig
  admin              Generate a kubeconfig file for the admin to use and for kubeadm itself
  all                Generate all kubeconfig files
  controller-manager Generate a kubeconfig file for the controller manager to use
  kubelet            Generate a kubeconfig file for the kubelet to use *only* for cluster bootstrapping purposes
  scheduler          Generate a kubeconfig file for the scheduler to use
```


生成所有配置文件
```sh
kubeadm init phase kubeconfig all
```

配置文件路径默认保存在
```
/etc/kubenetes/
```

### 4、生成kubelet配置文件，并重启kubelet

```sh
kubeadm init phase kubelet-start
```
创建出来的配置文件里的 clusterDNS 为默认的 10.96.0.10

```sh
/var/lib/kubelet/config.yaml      # 包含了 kubelet 的运行时配置，如 cgroup 驱动、证书位置、网络设置
```



---

### 5、创建pod清单

为 API 服务器、控制器管理器和调度器生成静态 Pod 的清单文件。
假使没有提供一个外部的 etcd 服务的话，也会为 etcd 生成一份额外的静态 Pod 清单文件。
静态 Pod 的清单文件被写入到 /etc/kubernetes/manifests 目录； 
kubelet 会监视这个目录以便在系统启动的时候创建 Pod。
**pod全都运行起来了，init流程才会继续**

```sh
kubeadm init phase control-plane all
```

启动 kube-scheduler、kube-apiserver、kube-controller-manager 这3个静态pod



### 6、创建 etcd

如果没有指定外部 etcd 集群，则创建本地 单节点 etcd 的pod

```sh
kubeadm init phase etcd local
```

### 7、


从配置文件生成 configmap
```sh
kubeadm init phase upload-config [command]
  all
  kubeadm
  kubelet
```



<!-- ### 5、为控制节点打污点
对控制平面节点应用标签和污点标记以便不会在它上面运行其它的工作负载

 -->

<!-- ### 6、生成令牌
将来其他节点可使用该令牌向控制平面注册自己，生成token，用于其他节点 kubeadm join

### 7、 

为了使得节点能够遵照启动引导令牌和 TLS 启动引导 这两份文档中描述的机制加入到集群中，kubeadm 会执行所有的必要配置：

创建一个 ConfigMap 提供添加集群节点所需的信息，并为该 ConfigMap 设置相关的 RBAC 访问规则。

允许启动引导令牌访问 CSR 签名 API。

配置自动签发新的 CSR 请求。

更多相关信息，请查看 kubeadm join。

### 8、
通过 API 服务器安装一个 DNS 服务器 (CoreDNS) 和 kube-proxy 附加组件。 在 Kubernetes 版本 1.11 和更高版本中，CoreDNS 是默认的 DNS 服务器。 请注意，尽管已部署 DNS 服务器，但直到安装 CNI 时才调度它。 -->







---
---
---

## 其他
token，用户加入集群使用
```sh
kubeadm token [选项]
    list      #查看token，24小时有效期
    create    #创建一个新的token
      --print-join-command   #打印完整的 kubeadm join 命令
               
```

重置kubeadm，但是不会清除iptables和ipvs，需要手动清除
```sh
kubeadm reset
```

清空iptables规则
```sh
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

重置 IPVS 表
```sh
ipvsadm -C
```
