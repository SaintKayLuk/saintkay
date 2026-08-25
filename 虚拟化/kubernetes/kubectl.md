## kubectl概述

使用 Kubectl 命令行工具管理 Kubernetes 集群

kubectl 在 $HOME/.kube 目录中查找一个名为 config 的配置文件
你可以通过设置 KUBECONFIG 环境变量

需要配置kubectl认证信息，两种方法

将/etc/kubernetes/admin.conf复制到$HOME/.kube/config，对于普通用户来说，用这种方法
```sh
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

设置环境变量KUBECONFIG，至于放哪个环境变量参数根据场景来设定
```sh
echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bash_profile
source ~/.bash_profile
```



## 安装kubectl

### 普通方式
* 下载 kubectl 最新版本

```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

$(curl -L -s https://dl.k8s.io/release/stable.txt) 是最新版本
```

* 下载kubectl 1.20.9 版本
```
curl -LO https://dl.k8s.io/release/v1.20.9/bin/linux/amd64/kubectl
```


* 校验kubectl（可选）下载的 kubectl 与校验文件版本必须相同。
```sh
#下载 kubectl 校验文件
curl -LO "https://dl.k8s.io/v1.20.9/bin/linux/amd64/kubectl.sha256"
#基于校验文件，验证 kubectl 可执行文件
echo "$(<kubectl.sha256) kubectl" | sha256sum --check
#验证通过时，输出为：
kubectl: OK
```

* 安装 kubectl
```sh
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

* 验证安装
```sh
kubectl version --client
```

### 基于redhat发行版
```
yum install -y kubectl-1.20.9
```

## kubectl自动补全

* 安装bash-completion
```sh
yum install -y bash-completion
#在文件 ~/.bashrc 中导入（source）补全脚本
echo 'source <(kubectl completion bash)' >>~/.bashrc
source ~/.bashrc
type _init_completion

#如果 type _init_completion 报错，则执行以下命令
source /usr/share/bash-completion/bash_completion
```

* 启动 kubectl 自动补全功能
```sh
kubectl completion bash >/etc/bash_completion.d/kubectl
```


## kubectl命令

```
kubectl [command] [TYPE] [NAME] [flags]
    command         指定要对一个或多个资源执行的操作
        explain         列出资源清单
        create          创建资源，源资源不删除，无法创建
        apply           更新资源，配置没有改变，则不会更新
        get             显示一个或多个资源
        describe        显示一个或多个资源的详细状态。
        delete          删除资源
        top             xxx
        exec            进入容器，或者进入容器执行命令
        set             修改pod模板下的资源
            image           修改镜像
            resources       修改资源要求
    TYPE            指定资源类型。资源类型不区分大小写，可以指定单数、复数或缩写形式
    NAME            指定资源的名称。名称区分大小写。 如果省略，则显示该类型所有资源

    flags           可选参数
        -s/server [ip:port]             指定 Kubernetes API 服务器的地址和端口
        -o/--output [output_format]     以特定格式向终端窗口输出详细信息
```


通过--help查看kubectl命令
```
kubectl --help          查看所有命令
kubectl get --help      查看get子命令      
```


### kubectl get

```
kubectl get [TYPE] [NAME] [flags]


    flags
        -n/--namespace [namespace]      查看指定命名空间
        -o/--ouput [output_format]      输出格式化
        --show-labels                   显示标签
        --all-namespaces                查看所有命名空间的资源
```

例
```
kubectl get pod,rs                      查看pod和rs

kubectl get pod                         查看default命名空间的pod
kubectl get pods -o wide                查看default命名空间的pod的详细信息
kubectl get pods -n kube-system         查看kube-system命名空间的pod

```
#### -o/--output

```
kubectl get [TYPE] [NAME] -o/--output [output_format]
    -o name     只显示资源名
    -o wide     纯文本显示，包含任何附加信息，对于 pod 包含节点名
    -o json     输出 JSON 格式的 API 对象
    -o yaml     输出 YAML 格式的 API 对象。
```

### kubectl exec

```
kubectl exec


例：进入名为 test 的pod容器用bash
kubectl exec test -it -- bash 
```


### kubectl label


1. 查看资源对象的label是get xxx 后面加 --show-labels 
2. kubectl label 设置和取消资源对象的 label 




### kubectl explain

通过 explan 列出资源选项

```sh
kubectl explain pods 
    --recursive       #列出此层级下所有资源

```


例：kubectl explain pod，列出pod的资源的选项，相当于当 Kind 为 Pod 的时候，能写的key是哪些，当然可以 kubectl explain pod.spec 来查看 pod.spec 下的资源清单
```
KIND:       Pod
VERSION:    v1

DESCRIPTION:
    Pod is a collection of containers that can run on a host. This resource is
    created by clients and scheduled onto hosts.
    
FIELDS:
  apiVersion    <string>
    APIVersion defines the versioned schema of this representation of an object.
    Servers should convert recognized schemas to the latest internal value, and
    may reject unrecognized values. More info:
    https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

  kind  <string>
    Kind is a string value representing the REST resource this object
    represents. Servers may infer this from the endpoint the client submits
    requests to. Cannot be updated. In CamelCase. More info:
    https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

  metadata      <ObjectMeta>
    Standard object's metadata. More info:
    https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

  spec  <PodSpec>
    Specification of the desired behavior of the pod. More info:
    https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

  status        <PodStatus>
    Most recently observed status of the pod. This data may not be up to date.
    Populated by the system. Read-only. More info:
    https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

```



### 与节点和集群交互


```sh
kubectl cordon my-node      # 标记 my-node 节点为不可调度，节点状态会多一个 SchedulingDisabled
kubectl uncordon my-node    # 标记 my-node 节点为可以调度，取消 SchedulingDisabled 状态

kubectl drain my-node       # 对 my-node 节点进行清空操作，为节点维护做准备


kubectl drain my-node --ignore-daemonsets --delete-emptydir-data --force
# --ignore-daemonsets         忽略 daemonset
# --delete-emptydir-data      即使 pod 使用了 emptydir 也继续
# --force                     清空没有被管理的pod，即单独运行的pod
```







