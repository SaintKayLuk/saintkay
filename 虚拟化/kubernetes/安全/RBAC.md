

* 相关的资源对象
  * User
  * ServiceAccount
  * Role
  * ClusterRole
  * RoleBinding
  * ClusterRoleBinding

## User 和 ServiceAccount


User 适用于使用 kubectl 来访问k8s
ServiceAccount 适用于 Pod 内部访问 K8s





## Role 和 ClusterRole

Role 针对某个命名空间的角色

kubectl 示例，创建 名为 test-role 的Role ，并且对 deployment 资源有 create 和 delete 的权限
```sh
kubectl create role test-role --resource=deploy --verb=create,delete
```



yaml 示例
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default    # 必须指定
  name: pod-reader
rules:
- apiGroups: [""] # "" 标明 core API 组，
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```


ClusterRole 针对集群的角色，不受命名空间影响
示例
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  # "namespace" 被忽略，因为 ClusterRoles 不受名字空间限制
  name: secret-reader
rules:
- apiGroups: [""]
  # 在 HTTP 层面，用来访问 Secret 资源的名称为 "secrets"
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```


apiGroups 就是对应的其他资源对象的 apiVersion ，如果 是v1，则就是 核心 API 组，例如pod，Service 等，如果是Deployment ，因为 Deployment 的yaml模板里是 apiVersion 是 apps/v1 则如果要添加 Deployment 的权限则这里的 apiGroups 就需要写 apiGroups: ["apps"]


## RoleBinding 和 ClusterRoleBinding


RoleBinding  可以绑定同命名空间的所有 Role 和 ClusterRole
ClusterRoleBinding 只能绑定 ClusterRole

RoleBinding 绑定 ClusterRole 则拥有 当前命名空间内的 ClusterRole 的权限，这样可以写一些通用的权限

RoleBinding 示例
```yaml
apiVersion: rbac.authorization.k8s.io/v1
# 此角色绑定允许 "jane" 读取 "default" 名字空间中的 Pod
# 你需要在该名字空间中有一个名为 “pod-reader” 的 Role
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
# 你可以指定不止一个“subject（主体）”
- kind: User
  name: jane # "name" 是区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  # "roleRef" 指定与某 Role 或 ClusterRole 的绑定关系
  kind: Role        # 此字段必须是 Role 或 ClusterRole
  name: pod-reader  # 此字段必须与你要绑定的 Role 或 ClusterRole 的名称匹配
  apiGroup: rbac.authorization.k8s.io
```

ClusterRoleBinding 示例
```yaml
apiVersion: rbac.authorization.k8s.io/v1
# 此集群角色绑定允许 “manager” 组中的任何人访问任何名字空间中的 Secret 资源
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
- kind: Group
  name: manager      # 'name' 是区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```










