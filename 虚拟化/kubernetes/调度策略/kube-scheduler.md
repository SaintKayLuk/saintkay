

kube-scheduler 是 kubernetes 的默认调度器，可以自己写一个调度器替换掉 kube-scheduler


## kube-scheduler调度流程

1. 过滤：过滤符合pod请求资源的node列表，如果此列表为0，则代表此pod不可调度
2. 打分



影响pod调度的因素
1. 直接指定node，通过 spec.nodeName
2. 通过node标签，通过 spec.nodeSelector
3. node亲和性，通过   spec.affinity.nodeAffinity
4. pod亲和性和反亲和性
5. pod的资源开销，例如规定pod的资源请求
6. node的污点和pod的容忍
7. pod的优先级，是否被高优先级pod抢占
8. 基于节点压力的驱逐
9. api发起的驱逐，例如**kubectl drain**




## pod开销

创建一个 RuntimeClass
设置由 哪个runtimeclass启动的pod额外占用多少内存和cpu
例如，一个pod里有一个容器，请求了200m内存，则如果由kata-fc启动，那这个pod需要320m内存

```yaml
kind: RuntimeClass
apiVersion: node.k8s.io/v1
metadata:
    name: kata-fc
handler: kata-fc
overhead:
    podFixed:
        memory: "120Mi"
        cpu: "250m"
```


