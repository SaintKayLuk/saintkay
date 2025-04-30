
## namespace

Kubernetes 支持多个虚拟集群，它们底层依赖于同一个物理集群。 这些虚拟集群被称为名字空间

```
[root@node-1 ~]# kubectl get namespace
NAME              STATUS   AGE
default           Active   24h
kube-node-lease   Active   24h
kube-public       Active   24h
kube-system       Active   24h
```

Kubernetes 会创建三个初始名字空间
* default：没有指明使用其它名字空间的对象所使用的默认名字空间
* kube-system：Kubernetes 系统创建对象所使用的名字空间
* kube-public： 这个名字空间是自动创建的，所有用户（包括未经过身份验证的用户）都可以读取它。 这个名字空间主要用于集群使用，以防某些资源在整个集群中应该是可见和可读的。 这个名字空间的公共方面只是一种约定，而不是要求。

查看命名空间

```sh
kubectl get namespace/ns
```

查看某个命名空间下的资源

```sh
kubectl get pods --namespace/-n 
```

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: xxx
```



删除命名空间会删除此命名空间下的所有资源
```sh
kubectl delete namespace xxx
```