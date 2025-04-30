


yaml示例
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Retain
allowVolumeExpansion: true
mountOptions:
  - debug
volumeBindingMode: Immediate
```


设置storageclass为默认，xxx为需要设置的 storageclass 的 name
```sh
kubectl annotate storageclass xxx storageclass.kubernetes.io/is-default-class=true
```

取消storageclass为默认，xxx为需要设置的 storageclass 的 name
```sh
kubectl annotate storageclass xxx storageclass.kubernetes.io/is-default-class-
```
