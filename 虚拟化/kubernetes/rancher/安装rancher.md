# 安装 Rancher

查看版本对应关系
https://www.suse.com/zh-cn/suse-rancher/support-matrix/all-supported-versions/rancher-v2-9-4/


文档链接
https://ranchermanager.docs.rancher.com/zh/v2.6/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster#ingress-controller


通过helm安装，默认镜像从 docker.io 拉取，可以先手动pull再改tag

```sh
# 下载镜像  rancher v2.8.5版本
ctr -n k8s.io image pull registry.cn-hangzhou.aliyuncs.com/saintkay/rancher:v2.8.5
ctr -n k8s.io image pull registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.shell:v0.1.24
ctr -n k8s.io image pull registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.gitjob:v0.9.8
ctr -n k8s.io image pull registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.fleet:v0.9.5
ctr -n k8s.io image pull registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.fleet-agent:v0.9.5
ctr -n k8s.io image pull registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.rancher-webhook:v0.4.7





```


```sh
# 修改tag
ctr -n k8s.io image tag registry.cn-hangzhou.aliyuncs.com/saintkay/rancher:v2.8.5 docker.io/rancher/rancher:v2.8.5
ctr -n k8s.io image tag registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.shell:v0.1.24 docker.io/rancher/shell:v0.1.24
ctr -n k8s.io image tag registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.gitjob:v0.9.8 docker.io/rancher/gitjob:v0.9.8
ctr -n k8s.io image tag registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.fleet:v0.9.5 docker.io/rancher/fleet:v0.9.5
ctr -n k8s.io image tag registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.fleet-agent:v0.9.5 docker.io/rancher/fleet-agent:v0.9.5
ctr -n k8s.io image tag registry.cn-hangzhou.aliyuncs.com/saintkay/rancher.rancher-webhook:v0.4.7 docker.io/rancher/rancher-webhook:v0.4.7






```



## 安装 cert-manager (可选)
如果在云上的集群，例如阿里云的ack，通过slb来负载均衡，默认是有证书


```sh
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

查看一下所有版本
```sh
helm search repo cert-manager --versions
```

安装
```sh
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true --version v1.12.17
```



## 安装 rancher


```sh
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
kubectl create namespace cattle-system


192.168.5.201.sslip.io

# 可以设置初始密码，如果没有设置初始密码，则通过 kubectl get secret --namespace cattle-system bootstrap-secret -o go-template='{{.data.bootstrapPassword|base64decode}}{{ "\n" }}' 来获取
helm install rancher rancher-stable/rancher --namespace cattle-system --set hostname=rancher.xxx.com  --set bootstrapPassword=admin --set ingress.tls.source=secret --version 2.8.5
```



helm install rancher rancher-stable/rancher --namespace cattle-system --set hostname=10.10.206.31.sslip.io  --set bootstrapPassword=admin --set ingress.tls.source=secret --version 2.8.5
