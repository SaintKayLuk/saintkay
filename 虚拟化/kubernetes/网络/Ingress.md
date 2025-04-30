# Ingress Controller

先安装 ingress-controller


版本对应关系文档
```
https://github.com/kubernetes/ingress-nginx/blob/main/README.md#readme
```

ingress-controller的yaml下载地址
```
https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.6/deploy/static/provider/cloud/deploy.yaml
```
镜像可以使用阿里云镜像，通过阿里云构建github地址的海外镜像
下载完之后，修改ingress-nginx.yaml文件，把镜像地址改为阿里云的地址




ingress-controller 的常见几种部署方式

### Deployment + LoadBalancer (云环境或本地)
1. 一般用于公有云等云上环境
2. 用 deployment 部署 igress-controller，并且对应的 service 的 type 使用 LoadBalancer
3. 大部分公有云，会为 LoadBalancer 的 service 自动创建一个负载均衡器，通常还绑定了公网地址。只需把域名解析指向公网地址
  
**云环境上有提供load balancer**
**本地环境没有load balancer，可以手动安装 MetalLB 来替代，见 [metallb](metallb.md)**


### Deployment + NodePort (本地环境或裸机集群)

1. 用 deployment 部署ingress-controller，并且对应的 service 的 type 为 NodePort
2. 集群每个node上都开放端口
3. 需要在外面再搭建一套负载均衡器来转发请求
4. NodePort多了一层NAT转发





### DaemonSet + HostNetwork
1. 用 DaemonSet 部署 ingress-controller，不创建service，pod直接使用宿主机 80/443 端口
2. 一个node只能部署一个ingress-controller pod
3. 使用物理机的DNS域名解析，而无法使用内部的比如coredns域名解析




# IngressClass


使用 Ingress 类在集群中部署任意数量的 Ingress 控制器。 
可以指定一个为默认

yaml示例
```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.1.3
  name: nginx
  annotations:
    ingressclass.kubernetes.io/is-default-class: "true"     #设置为集群默认Ingress类
spec:
  controller: k8s.io/ingress-nginx
```



# Ingress


ingress相当于一段nginx的配置模板，ingress-controller相当于一个nginx，读取ingress的配置
配置ingress相当于动态更新nginx的配置文件

**yaml示例**
```yaml
apiVersion: networking.k8s.io/v1        #api版本
kind: Ingress                           #资源类型为Ingress
metadata:
  name: test-ingress
  namespace: default
  annotations:                          # 注解
    nginx.ingress.kubernetes.io/whitelist-source-range: "192.168.1.1/32"  # 白名单
spec:
  ingressClassName: nginx               #指定IngressClass，如果不设置此值会用默认class，但是必须设置了默认class
  tls:                                  #设置https的证书
  - hosts:                            
      - https-example.foo.com           #域名，和下面的host一致
    secretName: testsecret-tls          #secret的name，此secrret里必须有tls.crt和tls.key
  rules:                                #转发规则
  - host:                               #域名绑定，相当于nginx的 server_name，未指定 host，则该规则适用于通过指定 IP 地址的所有
    http:
      paths:
      - path: "/"                       #同一个域名下可以设置多个path
        pathType: Prefix                #匹配类型 Prefix(前缀匹配，区分大小写)，Exact(精确匹配，区分大小写)
        backend:
          service: 
            name: my-service1           #service的名字
            port: 
              number: 8080              #service的端口
```


1. path 路径为 后端 pod 中的路径，例如后端 pod 为nginx，访问路径为 /aaa ，则path设置为 /aaa
2. 同一请求匹配到多条路径时，最长路径优先，如果仍存在两条匹配路径，则 Exact 优先于 Prefix


## ingress 注解


```yaml
# 白名单
nginx.ingress.kubernetes.io/whitelist-source-range: "192.168.1.1/32"


# 配置nginx与后端服务通信用什么协议，可选 HTTP、HTTPS、AUTO_HTTP、GRPC、GRPCS 和 FCGI。默认使用HTTP
nginx.ingress.kubernetes.io/backend-protocol: "HTTP" 


# ssl直通，让https流量直接转发到后端，而不不是让nginx来解密
nginx.ingress.kubernetes.io/ssl-passthrough: "true"
```