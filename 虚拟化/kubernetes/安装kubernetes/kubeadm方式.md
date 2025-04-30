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





## 创建集群

```sh
kubeadm init --apiserver-advertise-address xx.xx.xx.xx --image-repository registry.aliyuncs.com/google_containers --kubernetes-version v1.25.14 --service-cidr 10.20.0.0/16 --pod-network-cidr 10.10.0.0/16

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


#### 配置kubectl认证信息

```sh
echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bash_profile
source ~/.bash_profile
```

#### 添加网络插件

[安装 flannel](../网络/cni/flannel.md)
[安装 calico](../网络/cni/calico/安装calico.md)

#### 其他节点加入

```sh
kubeadm join 10.80.32.201:6443 --token kyx654.rqiydc2ptwicfmgp \
    --discovery-token-ca-cert-hash sha256:c41d60fbc8649ebd82f718a7768e6bba7ca42cdf90297dd839961893f6b1d462

#token失效重新获取
kubeadm token create --print-join-command
```
