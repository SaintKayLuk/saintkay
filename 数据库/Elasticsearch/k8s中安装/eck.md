# 安装 ECK


```sh
kubectl create -f https://download.elastic.co/downloads/eck/2.15.0/crds.yaml
```

```sh
kubectl apply -f https://download.elastic.co/downloads/eck/2.15.0/operator.yaml
```




## 安装 elasticsearch

## 安装kibana


如果使用 ingress 来访问 kibana，因为默认是https的，所以需要添加注解，并且指定自己的域名的证书

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: HTTPS
    nginx.ingress.kubernetes.io/ssl-passthrough: 'true'
    ...
```