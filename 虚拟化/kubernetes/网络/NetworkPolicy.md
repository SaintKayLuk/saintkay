## 网络策略

针对pod 的访问隔离，类似于 阿里云的安全组，但是是针对 pod 的

Pod 有两种隔离: 出口的隔离和入口的隔离，默认都不隔离，如果添加了 policyTypes 之后，添加了




yaml示例
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:                          # pod 标签选择器，这些pod设置网络策略
    matchLabels:
      app: nginx
  policyTypes:                          # 设置策略，添加 Ingress 则入口隔离。添加 Egress 则出口隔离
    - Ingress
    - Egress
  ingress:                              # 具体的 入口隔离的策略
    - from:
        - ipBlock:
            cidr: 172.17.0.0/16
            except:
              - 172.17.1.0/24
        - namespaceSelector:
            matchLabels:
              project: myproject
        - podSelector:
            matchLabels:
              role: frontend
      ports:                            # 设置端口，如果不设置，则所有端口都不限制，但是受限于 from
        - protocol: TCP
          port: 6379
  egress:                               # 具体的出口隔离策略
    - to:
        - ipBlock:
            cidr: 10.0.0.0/24
      ports:                            # 设置端口，如果不设置，则所有端口都不限制，但是受限于 to
        - protocol: TCP
          port: 5978
```


### 默认策略

默认是不存在 NetworkPolicy de，如果要设置如有的pod的 入口策略为拒绝，则可以这么设置
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```


设置允许所有入站流量，当然默认就是这个策略，虽然没有 default NetworkPolicy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - {}
```


出站的yaml文件同理
