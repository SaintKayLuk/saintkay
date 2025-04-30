# 安装redis




## 在k8s中安装


#### helm 方式


#### operator 方式


**前提条件**：redis-operator 可能用到 prometheus ，需要先安装一下，如果有则不需要安装，或者在redis-operator中删除对应内容
```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
# 验证一下
kubectl get crds | grep monitoring.coreos.com
```

或者手动安装
```sh
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
```


1. 安装 redis-operator

通过helm 来安装目前有问题，后期验证
<!-- 通过 helm 来安装 redis-operator
```sh
helm repo add redis-operator https://spotahome.github.io/redis-operator
helm repo update
helm install redis-operator redis-operator/redis-operator
``` -->

或者通过 yaml 文件来安装，两个文件
[redisfailovers.yaml](./yaml文件/databases.spotahome.com_redisfailovers.yaml)
[redis-operaotr](./yaml文件/all-redis-operator-resources.yaml)
```sh
kubectl apply -f https://raw.githubusercontent.com/spotahome/redis-operator/v1.3.0-rc1/manifests/databases.spotahome.com_redisfailovers.yaml
kubectl apply -f https://raw.githubusercontent.com/spotahome/redis-operator/v1.3.0-rc1/example/operator/all-redis-operator-resources.yaml
# 下载不到文件，手动上传执行
kubectl apply -f databases.spotahome.com_redisfailovers.yaml
kubectl apply -f all-redis-operator-resources.yaml
```


2. 通过自定义资源安装redis

[custon-redis](./yaml文件/custom-redis.yaml)
```sh
kubectl apply -f custon-redis.yaml
```

这种方式安装的默认属于主从，连接可以通过 sentinel 来连，

	
rfrm-redisfailover：redis主的service，
rfrs-redisfailover：redis从的service
rfs-redisfailover：redis的sentinel的service，如果代码是通过sentinel连接，则选择这个


3. 删除redis

```sh
kubectl delete -n xxx RedisFailover xxx
```

#### 直接安装

简单示例：
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: base
spec:
  replicas: 1  # 只需一个 Redis 实例，即单节点
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: docker.io/redis:6.2.16
          ports:
            - containerPort: 6379  # Redis 默认端口
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: base
spec:
  selector:
    app: redis
  ports:
    - port: 6379  # 服务端口
      targetPort: 6379  # Pod 端口
  type: ClusterIP
```








