# helm 命令


## helm repo

helm仓库命令

```sh
helm repo [command]
    list                    # 查看本地仓库列表
    update                  # 更新本地仓库的可用chart
    add [仓库] [仓库地址]
    remove [仓库]
    
```

例：添加仓库，**此仓库可能已经弃用，这里只是个例子**
```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
```

例：删除仓库
```sh
helm repo remove bitnami
```

## helm search

helm搜索命令

```sh
helm search [command] [chart]
    hub     # 从 Artifact Hub 查找chart
    repo    # 在本地已经添加的仓库中查找chart
        <chart-name> --versions     # 查看本地仓库中chart的所有版本
```

例：列出mysql的所有版本
```sh
helm search repo mysql --versions
```

## helm install

安装一个chart


```sh
helm install [name] [chart]
    -n/--namespace          #指定命令空间
    --create-namespace      #如果指定的命名空间不存在则创建
    --generate-name         #如果没有指定name，则随机生成一个
```

如果不指定chart的名字，则可以用 --generate-name 来生成名字
```sh
helm install [chart] --generate-name
```



例：各种安装chart方式
```sh
#通过chart引用： 
helm install mymaria example/mariadb

#通过chart包： 
helm install mynginx ./nginx-1.2.3.tgz

#通过未打包chart目录的路径： 
helm install mynginx ./nginx

#通过URL绝对路径： 
helm install mynginx https://example.com/charts/nginx-1.2.3.tgz

#通过chart引用和仓库url： 
helm install --repo https://example.com/charts/ mynginx nginx

#通过OCI注册中心： 
helm install mynginx --version 1.2.3 oci://example.com/charts/nginx
```


## helm uninstall

卸载一个 chart

```sh
helm uninstall [chart]
```


## helm pull

下载chart的压缩包到本地

```sh
helm pull [chart URL | repo/chartname] [...] [flags]
    flags
        --version xxx   # 下载指定版本

```

一般我们解压出来，修改values.yaml 文件，然后再部署

在当前路径下执行
```sh
helm install xxx .
```


## helm inspect 

查看 values 配置文件 的详解
```sh
helm inspect values hashicorp/consul
```

