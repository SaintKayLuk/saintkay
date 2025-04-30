## ReplicaSet

ReplicaSet 确保任何时间都有指定数量的 Pod 副本在运行

* 一定数量副本数
* 完全相同pod
* 无状态

1. 如果直接创建裸pod， 且标签 被 ReplicaSet 的标签选择器选中，则会被此 ReplicaSet 管理，并且影响原来的 ReplicaSet 副本数
2. replicaset里面的pod是属主此replicset的，如果其他控制器下的pod标签被此replicaset选中也不会被管理，因为有各自的属主，只能管理此文件下的pod和裸pod
3. 默认删除 ReplicaSet 资源，会删除被此 ReplicaSet 管理的pod

yaml示例

```yaml
apiVersion: apps/v1             
kind: ReplicaSet                #指定资源类型为 ReplicaSet
metadata:
  name: frontend                #名字
  labels:                       #标签，ReplicaSet的标签
    app1: abc
    app2: bbb
spec:
  replicas: 3                   #指定要同时运行的 Pod 个数，不指定，默认为1
  selector:                     #标签选择器，.spec.selector 必须匹配 .spec.template.metadata.labels
    matchLabels:
      app: xxx                  #选择标签有 app=xxx 的pod
  template:                     #pod模板
    metadata:
      labels:                   #模板pod的标签
        app: xxx                #在此模板中，即template下的pod，此标签必须要和spec.selector一致，否则会被api拒绝
    spec:                       
      containers:               #容器内容，名字，镜像等
      - name: pod-test
        image: test:v3
        restartPolicy: Always   #重启策略，唯一取值，不用写
```

例：查看replicaset

```
kubectl get rs
NAME                  DESIRED   CURRENT   READY   AGE
frontend              3         3         3       41s

NAME          列出replicaset名字
DESIRED       期望副本数
CURRENT       当前运行状态中的副本数
READY         有多少副本可提供服务
AGE           运行时间
```