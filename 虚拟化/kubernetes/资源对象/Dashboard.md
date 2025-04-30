# Dashboard

Kubernetes 仪表板

查看版本兼容关系
```
https://github.com/kubernetes/dashboard/releases
```

k8s 1.25版本 Dashboard v2.7.0



## 创建 访问用户

文档链接
```
https://github.com/kubernetes/dashboard/blob/v2.7.0/docs/user/access-control/creating-sample-user.md
```

创建权限
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
#Creating a ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

### 生成临时token
```sh
kubectl -n kubern etes-dashboard create token admin-user
```

### 生成长久token

创建一个secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: admin-user-token
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: "admin-user"  # 绑定到已有的 ServiceAccount
type: kubernetes.io/service-account-token
```

获取token
```sh
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
```