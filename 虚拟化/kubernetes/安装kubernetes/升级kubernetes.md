# kubeadm 方式升级

只能升级一个版本，例如1.18升级到1.19，不能从1.18直接升级到1.24

例：从 1.20 升级到 1.21

1. 升级控制节点
```sh
#列出 kubeadm 所有版本
yum list --showduplicates kubeadm --disableexcludes=kubernetes
# 升级 kubeadm
yum install -y kubeadm-1.21.14 --disableexcludes=kubernetes
# 验证当前 kubeadm 版本
kubeadm version
# 验证升级计划
kubeadm upgrade plan
# 根据升级计划升级
kubeadm upgrade apply v1.21.14

# 腾空节点
kubectl drain <节点名称> --ignore-daemonsets
# 升级 kubelet 和 kubectl
yum install -y kubelet-1.21.14 kubectl-1.21.14 --disableexcludes=kubernetes
systemctl daemon-reload
systemctl restart kubelet
# 解除节点保护
kubectl uncordon <节点名称>
```


2. 手动升级 cni 插件
3. 升级其他 控制节点 **(多个控制节点的情况)**
```sh
yum install -y kubeadm-1.21.14 --disableexcludes=kubernetes
kubeadm upgrade node

kubectl drain <节点名称> --ignore-daemonsets

yum install -y kubelet-1.21.14 kubectl-1.21.14 --disableexcludes=kubernetes
systemctl daemon-reload
systemctl restart kubelet

kubectl uncordon <节点名称>
```
4. 升级 worker 节点
```sh
yum install -y kubeadm-1.21.14 --disableexcludes=kubernetes
kubeadm upgrade node

kubectl drain <节点名称> --ignore-daemonsets

yum install -y kubelet-1.21.14 kubectl-1.21.14 --disableexcludes=kubernetes
systemctl daemon-reload
systemctl restart kubelet

kubectl uncordon <节点名称>
```
5. 验证集群
```sh
# 查看 status 是否为 REDAY ，并且版本号已经升级
kubectl get nodes
```
