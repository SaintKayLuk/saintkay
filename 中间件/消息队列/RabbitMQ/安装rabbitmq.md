# 安装 rabbitMQ


docker镜像版本，不同后缀区别

* xxx-management：包含管理插件，标准基础镜像。
* xxx-management-alpine：包含管理插件，基于 Alpine 的镜像。
* xxx-alpine：不包含管理插件，基于 Alpine 的镜像。
* xxx：不包含管理插件，标准基础镜像


## 在k8s中安装



```sh
kubectl apply -f https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml
```
下载不了直接查看[cluster-operator.yml](./yaml文件/cluster-operator.yml)


然后执行自定义的资源文件，例如 [rabbitmq-cluster.yaml](./yaml文件/rabbitmq-cluster.yaml)


获取用户名密码，集群安装完默认的用户名密码
```sh
kubectl -n rabbitmq-system get secret rabbitmq-cluster-default-user -o jsonpath="{.data.username}" | base64 --decode
kubectl -n rabbitmq-system get secret rabbitmq-cluster-default-user -o jsonpath="{.data.password}" | base64 --decode

# 如果是BusyBox基础容器，则 --decode 换成 -d

kubectl -n rabbitmq-system get secret rabbitmq-cluster-default-user -o jsonpath="{.data.username}" | base64 -d
kubectl -n rabbitmq-system get secret rabbitmq-cluster-default-user -o jsonpath="{.data.password}" | base64 -d
```


### 删除 

rabbitmq-cluster 为定义的名字
```sh
kubectl delete rabbitmqcluster rabbitmq-cluster -n rabbitmq-system
```









