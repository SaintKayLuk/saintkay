## Deployment

Pod <-- ReplicaSet(RS) <-- Deployment
* deployment 管理 replicaset， 并通过 replicaset 管理 pod
* 不建议直接操作 deployment 管理的 replicaset
* 生成的 replicaset 名字为 [Deployment名称]-[随机字符串]
* 生成的 pod 的名字为 [Deployment名称]-[随机字符串]-[随机字符串]，即[Replicaset名称]-[随机字符串]

yaml示例
```yaml
apiVersion: apps/v1           
kind: Deployment              #定义资源类型
metadata:
  name: nginx-deployment      #定义 deployment 名字
  labels:                     #deployment标签
    app: nginx
spec:                         #和replicaset一样，下面内容就是replicaset的定义
  replicas: 3                 #定义副本数量
  revisionHistoryLimit: 10    #保留的ReplicaSet版本，即历史版本，默认10个，加上当前运行的rs和历史10个rs最多保留11个rs，如果设置为0，则不会保留rs，则不能回滚
  strategy:                   #更新策略
    type: RollingUpdate       #新 Pods 替换旧 Pods 的策略,Recreate(启动新pod前会停止旧pod)和RollingUpdate(默认，先启动新pod再停止旧pod)
    rollingUpdate:              
      maxUnavailable: 25%     #最大不可用，更新过程中不可用的 Pod 的个数上限，可以指定数字也可以用百分比，默认25%
      maxSurge: 25%           #最大峰值，可以创建的超出 期望 Pod 个数的 Pod 数量，可以指定数字也可以用百分比，默认25%
  selector:                   #标签选择器，.spec.selector 必须匹配 .spec.template.metadata.labels
    matchLabels:
      app: nginx
  template:                   #pod模板，以下改变时，会触发deployment上线(模板标签或者容器镜像改变等，其他改变也会更新，但无意义)
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

例：查看deployment

```
kubectl get deploy
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           15h

NAME          集群中deployment的名字  
READY         就绪个数/期望个数
UP-TO-DATE    为了达到期望状态已经更新的副本数
AVAILABLE     可用副本数
AGE           运行时间
```

### 更新deployment

更改 .spec.template下的内容，会触发上线行为，即新建一个replicatset，逐步替换旧的replicaset，

在线编辑deployment
```sh
kubectl kubectl edit deployment/[deployment名字]
```

查看状态
```sh
kubectl rollout status deployment/[deployment名字]
```

例：更新deployment，更新镜像
```sh
kubectl set image deployment/my-deployment my-container=nginx:1.25.0
```

#### 更新策略 

* pod替换 .spec.strategy.type ,Recreate(启动新pod前会停止旧pod)和RollingUpdate(默认，先启动新pod再停止旧pod)
  * RollingUpdate：先启动新pod再停止旧pod
  * Recreate：先停止旧pod再启动新pod
* 更新pod数 .spec.strategy.rollingUpdate，两者不能同时为0，否则不能更新
  * .maxUnavailable：最大不可用数，百分比值会转换成绝对数并去除小数部分，
  * .maxSurge：最大峰值，百分比值会通过向上取整转换为绝对数


### 回滚deployment

deployment每次上线都会被记录在内，(spec.template改变)，通过 kubectl rollout history 查看

例：查看deployment历史版本

```
kubectl rollout history deployment/[deployment名字]

REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1 --record=true
3         kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1 --record=true
```

例：查看deployment第二个历史版本详细信息

```
kubectl rollout history deployment/[deployment名字] -resivion=2
```

例：回滚版本

```
回滚上一个版本
kubectl rollout undo deployment/[deployment名字]

回滚指定版本
kubectl rollout undo deployment/[deployment名字] --to-revision=2
```

### 缩放deployment

更改副本数量为10
```sh
kubectl scale deployment/nginx-deployment --replicas=10
```

**pod水平自动缩放**

### 暂停、恢复deployment

对deployment的暂停会不触发上线，即使更改了 .spec.template 的内容也不会触发上线，也不会增加历史版本，而原有服务还能正常运行

```sh
kubectl rollout pause deployment.v1.apps/nginx-deployment

kubectl rollout resume deployment.v1.apps/nginx-deployment
```