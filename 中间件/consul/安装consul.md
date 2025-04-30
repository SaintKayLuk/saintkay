# 安装 consul



## k8s中安装


#### 通过 Consul K8s CLI 安装



#### 通过 helm 安装

添加仓库
```sh
helm repo add hashicorp https://helm.releases.hashicorp.com
```

默认创建
```sh

helm install consul hashicorp/consul --set global.name=consul --create-namespace --namespace consul
```



先查看所有consul的版本
```sh
helm search repo consul --versions
```

安装 consul
```sh
export VERSION=1.5.6
helm install consul hashicorp/consul \
    --set global.name=consul \
    --version ${VERSION} \              # 指定版本
    --create-namespace \                # 不存在命名空间则创建
    --namespace consul                  # 指定命名空间
    --values values.yaml                # 指定配置文件
```


指定values.yml文件安装

```sh
helm show values hashicorp/consul > values.yaml

### ...
### 修改文件内容
### ...

# 指定配置文件
helm install consul hashicorp/consul --namespace consul --create-namespace -f values.yaml
```




#### 通过 Manifest 安装




