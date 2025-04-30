# node



## 污点

node的一个属性，可以有多个，为了某些不能容忍此污点的pod不被调度到节点上

```


添加污点
kubectl taint nodes [node_name] key=value:effect
删除污点
kubectl taint nodes [node_name] key=value:effect-
查看污点
kubectl describe node [node_name] |grep Taint


例：给node1节点添加一个key1=value1:NoSchedule的污点
kubectl taint nodes node1 key1=value1:NoSchedule
```


## ROLES

通过 kubectl get node 查看的时候的 roles，其实这个roles只是个label，并不作为判断node是否是worker节点的依据，通过设置node的label实现
```
kubectl get node
NAME    STATUS   ROLES                  AGE   VERSION
k8s-3   Ready    control-plane,master   93m   v1.20.11
k8s-4   Ready    worker                 89m   v1.20.11
```

node的label的key为node-role.kubernetes.io就是roles
```sh
#添加k8s-4节点的ROLE标签为worker
kubectl label nodes k8s-4 node-role.kubernetes.io/worker=

#删除k8s-4节点的ROLE标签
kubectl label nodes k8s-4 node-role.kubernetes.io/worker-
```




