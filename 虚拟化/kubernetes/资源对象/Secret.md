


https证书示例：key必须是 tls.crt 和 tls.key
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: testsecret-tls
  namespace: default
data:
  tls.crt: base64 编码的 cert
  tls.key: base64 编码的 key
type: kubernetes.io/tls
```

docker仓库凭证示例，secret区分namespace
```sh
kubectl create secret docker-registry secret名字 \ 
  --namespace=命名空间  \ 
  --docker-server=仓库地址 \
  --docker-username=用户名 \ 
  --docker-password=密码
```
