# StorageClass


yaml示例
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: low-latency
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"   # 设置为默认 StorageClass
provisioner: csi-driver.example-vendor.example            # 制备器，用来决定使用哪个卷插件制备 PV
reclaimPolicy: Retain                                     # 回收策略，Delete 或者 Retain，默认 Delete
allowVolumeExpansion: true                  # 卷支持卷扩展
mountOptions:
  - discard                                 # 这可能会在块存储层启用 UNMAP/TRIM
volumeBindingMode: WaitForFirstConsumer     # 卷绑定模式 Immediate(默认) 和 WaitForFirstConsumer
parameters:
  guaranteedReadWriteLatency: "true"        # 这是服务提供商特定的


```
## 回收策略 reclaimPolicy

Delete(默认) 或者 Retain

动态创建的pv会继承，除非pv显性指定自己的 persistentVolumeReclaimPolicy

删除PVC后
* Delete：PV通常会被删除，底层存储通常也会被删除，取决于存储驱动
* Retain：PV 通常进入 Released 状态，底层存储保留，通常需要人工清理或重新处理


## 卷绑定模式 volumeBindingMode

Immediate(默认) 和 WaitForFirstConsumer

* Immediate：创建 PVC 后，立即尝试绑定 PV 或动态创建存储
* WaitForFirstConsumer：等到有 Pod 使用该 PVC，再结合 Pod 的调度条件绑定或创建存储








## 注解部分

设置storageclass为默认，xxx为需要设置的 storageclass 的 name
```sh
kubectl annotate storageclass xxx storageclass.kubernetes.io/is-default-class=true
```

取消storageclass为默认，xxx为需要设置的 storageclass 的 name
```sh
kubectl annotate storageclass xxx storageclass.kubernetes.io/is-default-class-
```
