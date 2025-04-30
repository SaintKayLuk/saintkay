# 安装calico

两种方式，现在官方推荐先安装 Tigera operator


## 通过 Tigera Calico Operator 安装

先安装 tigera operator，如果文件下载不到，则手动上传
```sh
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.2/manifests/tigera-operator.yaml
```

安装自定义资源，可以根据需求修改内容
```sh
wget https://raw.githubusercontent.com/projectcalico/calico/v3.25.2/manifests/custom-resources.yaml
```


修改自定义资源，例如 cidr 改为自己集群的 pod 所在的网段


**手动下载镜像，有可能可以修改custom-resources.yaml 或者 tigera-operator.yaml，修改默认镜像拉取地址，后期验证**

因为通过 operator 去管理，默认 calico 各个镜像都从 docker.io 下载，手动下载完之后改tag

```sh
# 下载镜像
ctr -n k8s.io image pull quay.io/calico/node:v3.25.2
ctr -n k8s.io image pull quay.io/calico/pod2daemon-flexvol:v3.25.2
ctr -n k8s.io image pull quay.io/calico/cni:v3.25.2
ctr -n k8s.io image pull quay.io/calico/csi:v3.25.2
ctr -n k8s.io image pull quay.io/calico/node-driver-registrar:v3.25.2
ctr -n k8s.io image pull quay.io/calico/kube-controllers:v3.25.2
ctr -n k8s.io image pull quay.io/calico/typha:v3.25.2
ctr -n k8s.io image pull quay.io/calico/apiserver:v3.25.2

# 修改tag
ctr -n k8s.io image tag quay.io/calico/node:v3.25.2 docker.io/calico/node:v3.25.2
ctr -n k8s.io image tag quay.io/calico/pod2daemon-flexvol:v3.25.2 docker.io/calico/pod2daemon-flexvol:v3.25.2
ctr -n k8s.io image tag quay.io/calico/cni:v3.25.2 docker.io/calico/cni:v3.25.2
ctr -n k8s.io image tag quay.io/calico/csi:v3.25.2 docker.io/calico/csi:v3.25.2
ctr -n k8s.io image tag quay.io/calico/node-driver-registrar:v3.25.2 docker.io/calico/node-driver-registrar:v3.25.2
ctr -n k8s.io image tag quay.io/calico/kube-controllers:v3.25.2 docker.io/calico/kube-controllers:v3.25.2
ctr -n k8s.io image tag quay.io/calico/typha:v3.25.2 docker.io/calico/typha:v3.25.2
ctr -n k8s.io image tag quay.io/calico/apiserver:v3.25.2 docker.io/calico/apiserver:v3.25.2 
```


最后加载自定义资源文件，启动calico
```sh
kubectl create -f custom-resources.yaml
```

此方法因为 docker.io 镜像地址访问不到，比较麻烦，需要手动下载镜像并且修改tag

## 通过 Manifest 文件安装 Calico


直接一条命令
```sh
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.2/manifests/calico.yaml
```

当然，需要修改pod的id 和 镜像地址
```sh
wget https://raw.githubusercontent.com/projectcalico/calico/v3.25.2/manifests/calico.yaml

kubectl create -f calico.yaml
```







