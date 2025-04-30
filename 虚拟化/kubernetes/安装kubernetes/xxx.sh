#!/bin/bash

### 允许 iptables 检查桥接流量，开启ip4路由转发

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

#加载内核模块
sudo modprobe overlay
sudo modprobe br_netfilter


# 设置所需的 sysctl 参数，参数在重新启动后保持不变
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

# 应用 sysctl 参数而不重新启动
sysctl --system


tar Czxvf / cri-containerd-1.6.20-linux-amd64.tar.gz


mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml


sed -i 's/registry.k8s.io/registry.aliyuncs.com\/google_containers/g' /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml

systemctl enable containerd --now


apt update && apt install -y apt-transport-https

curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add - 

cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF

apt update



apt install -y kubelet=1.25.14-00
apt install -y kubectl=1.25.14-00
apt install -y kubeadm=1.25.14-00


systemctl enable kubelet

