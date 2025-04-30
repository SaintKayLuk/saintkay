# 安装nacos


## 在k8s中安装


#### 直接安装
有mysql则直接用，没有则安装

资源文件：[nacos.yaml](./yaml文件/nacos.yaml)


<!-- #### 通过operator安装

先安装operator
```sh
kubectl apply -f nacos-operator-all.yaml
```
[nacos-operator-all.yaml](./yaml文件/nacos-operator-all.yaml)


再安装自定义资源

```sh
kubectl apply -f nacos_cluster.yaml
``` -->