# DaemonSet

在每个 node 上运行一个 pod 副本
如果集群中新加入一个node，这daemonset会在此node上也运行一个pod副本


yaml示例
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: test-daemon
spec:
  selector:                         
    matchLabels:
      name: daemon-test             
  template:                         #pod模板
    metadata:
      labels:
        name: daemon-test           #标签
    spec:
      hostNetwork: true             #使用宿主机网络，相当于直接占用宿主机端口          
      tolerations:                  #可以设置一个key为空，op为Exists的容忍来容忍所有污点
      - key:
        operator: Exists                 
      containers:                   #容器
      - name: xxx
        image: k8s.io/xxx:v2.5.2
```

由daemonset创建的pod自带6个容忍
```
node.kubernetes.io/disk-pressure:NoSchedule op=Exists
node.kubernetes.io/memory-pressure:NoSchedule op=Exists
node.kubernetes.io/not-ready:NoExecute op=Exists
node.kubernetes.io/pid-pressure:NoSchedule op=Exists
node.kubernetes.io/unreachable:NoExecute op=Exists
node.kubernetes.io/unschedulable:NoSchedule op=Exists
```