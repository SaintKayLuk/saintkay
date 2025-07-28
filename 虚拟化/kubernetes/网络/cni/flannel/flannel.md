## flannel


```sh
wget https://github.com/flannel-io/flannel/releases/download/v0.25.6/kube-flannel.yml

#下载到本地，修改 Network 的值和 kubeadm --pod-network-cidr 的值一样

kubectl apply -f kube-flannel.yml


# kubelet 默认从 /etc/cni/net.d 下读取配置文件
# cni 插件默认位于 /opt/cni/bin
#https://v1-20.docs.kubernetes.io/zh/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/#cni
```
