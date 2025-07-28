## [准备工作](准备工作.md)


#### 安装 kubeadm,kubelet,kubectl

有依赖关系，按顺序安装
```sh
yum install -y kubelet-1.25.14
yum install -y kubectl-1.25.14
yum install -y kubeadm-1.25.14

#可以查询下可安装版本
apt-cache madison kubelet
#安装指定版本
apt install -y kubelet=1.25.14-00
apt install -y kubectl=1.25.14-00
apt install -y kubeadm=1.25.14-00


systemctl enable kubelet --now
```


#### 导入镜像(可选)

如果镜像拉取不到，可以手动导入

下载镜像和更改tag
```sh
# 下载镜像
kubeadm config images pull --kubernetes-version v1.25.14 --image-repository registry.aliyuncs.com/google_containers/


# 修改tag
ctr images tag registry.aliyuncs.com/google_containers/kube-apiserver:v1.25.14 registry.k8s.io/kube-apiserver:v1.25.14
ctr images tag registry.aliyuncs.com/google_containers/kube-controller-manager:v1.25.14 registry.k8s.io/kube-controller-manager:v1.25.14
ctr images tag registry.aliyuncs.com/google_containers/kube-scheduler:v1.25.14 registry.k8s.io/kube-scheduler:v1.25.14
ctr images tag registry.aliyuncs.com/google_containers/kube-proxy:v1.25.14 registry.k8s.io/kube-proxy:v1.25.14
ctr images tag registry.aliyuncs.com/google_containers/pause:3.8 registry.k8s.io/pause:3.8
ctr images tag registry.aliyuncs.com/google_containers/etcd:3.5.6-0 registry.k8s.io/etcd:3.5.6-0
ctr images tag registry.aliyuncs.com/google_containers/coredns:v1.9.3 registry.k8s.io/coredns/coredns:v1.9.3
```

导出导入
```sh
# 导出为 tar
ctr images export k8s-images-v1.25.14.tar   registry.k8s.io/kube-apiserver:v1.25.14   registry.k8s.io/kube-controller-manager:v1.25.14   registry.k8s.io/kube-scheduler:v1.25.14   registry.k8s.io/kube-proxy:v1.25.14   registry.k8s.io/pause:3.8   registry.k8s.io/etcd:3.5.6-0   registry.k8s.io/coredns/coredns:v1.9.3


# 导入到 k8s.io 下
sudo ctr --namespace k8s.io images import k8s-images-v1.25.14.tar
```


待验证-- 好像是每80天自动续签
**kubeadm 创建的集群 证书默认有效期为1年，但它调用的是 Golang 的 cfssl 生成证书，可以通过环境变量或 patch 工具实现证书有效期的控制。可以提前境变量方式修改证书默认有效期**
```sh
export KUBEADM_CERTIFICATE_DURATION="87600h"
```



## 创建集群 

```sh
kubeadm init --apiserver-advertise-address xx.xx.xx.xx --image-repository registry.aliyuncs.com/google_containers --kubernetes-version v1.25.14 --pod-network-cidr 10.10.0.0/16 --service-cidr 10.20.0.0/16 

...
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.80.32.201:6443 --token kyx654.rqiydc2ptwicfmgp \
    --discovery-token-ca-cert-hash sha256:c41d60fbc8649ebd82f718a7768e6bba7ca42cdf90297dd839961893f6b1d462 
```


#### 创建集群 - 配置文件方式


先创建一个默认的 kubeadm.yaml 的配置文件，修改此配置文件，相当于 init 后面添加的一些参数，例如 --image-repository 和 --pod-network-cidr 等
```sh
kubeadm config print init-defaults > kubeadm.yaml
```

创建集群指定配置文件
```sh
kubeadm init --config kubeadm.yaml
```


#### 配置kubectl认证信息

```sh
echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bash_profile
source ~/.bash_profile

# 有些系统默认不存在 ~/.bash_profile 文件，如果把 kubectl 认证信息写入 ~/.bash_profile 文件的话，会引起登录配置文件调用链问题
# 所以我们可以把 kubectl 认证信息 写入到 ~/.bashrc 中
echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bashrc
source ~/.bashrc
```

[登录的配置文件调用链关系](../../../计算机基础/linux/配置文件.md)

#### 添加网络插件

[安装 flannel](../网络/cni/flannel/flannel.md)
[安装 calico](../网络/cni/calico/安装calico.md)

#### 其他节点加入

```sh
kubeadm join 10.80.32.201:6443 --token kyx654.rqiydc2ptwicfmgp \
    --discovery-token-ca-cert-hash sha256:c41d60fbc8649ebd82f718a7768e6bba7ca42cdf90297dd839961893f6b1d462

#token失效重新获取
kubeadm token create --print-join-command
```
