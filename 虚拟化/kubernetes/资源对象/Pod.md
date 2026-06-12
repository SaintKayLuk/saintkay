## Pod

pod是kubernetes的最小单元，包括了一个或多个容器，以及共享资源。

Pod 天生地为其成员容器提供了两种共享资源：网络和 存储
即每个pod内
* 共享存储，数据卷
* 共享网络（ip和端口）


**yaml示例**
```yaml
apiVersion: v1                      #apiVersion版本，pod类型用v1，通过kubectl apiversion查看支持版本
kind: Pod                           #指定此yaml文件的资源类型
metadata:                       
  name: nginx-demo                  #pod名字
  namespace: awesomeapps            #命名空间，不填写就默认default空间
  labels:                           #pod的标签。可以设置多个标签
    app: v1.1                       #设置的标签，相当于app=v1.1
spec:
  initContainers:                   #init容器
  - name: init-myservice
    image: busybox:1.28
    command: ['xxx']
  containers:                       #应用容器设置
  - name: nginx                     #容器名   (如果要一个pod内启动多个应用容器，则可以设置多个name)
    image: nginx:1.14.2             #镜像名，版本
    imagePullPolicy: IfNotPresent   #镜像拉取策略 IfNotPresent(默认，在镜像存在时kubelet将不再去拉取镜像)，Never(从不主动拉取)，Always(每次拉取)
    ports:                          #端口设置
    - name: xxx-port                #容器端口名
      containerPort: 8080           #容器端口
      hostPort: 8080                #容器在节点上开放的端口，(如果设置了此端口，则会占用节点端口，此节点上就不能起2个容器)
      protocol: TCP                 #端口协议，TCP(默认)和STCP和UDP
    resources:                      #资源限制(默认没有限制能使用节点所有资源)
      requests:                     #请求资源(必须要这些资源)
        cpu: "0.5"                  #cpu核数(超线程指线程数)这里指0.5个cpu(1个cpu相当于裸机上具有超线程能力的英特尔处理器上的 1 个超线程)
        memory: 100M                #默认是字节，可以带单位(G、M、K)
      limits:                       #限制资源(最多能用这些资源)
        cpu: "3"                    
        memory: 200M
    livenessProbe:                  #存活探针(检测容器是否存活，三种检测方式只能存在一种)
      exec:                         #定义一个命令，返回非0则失败
        command:                    #具体的命令
        - cat
        - /tmp/healthy
      httpGet:                      #定义一个http请求
        path: /healthz              #请求地址
        port: 8080                  #请求端口,可以使用spec.containers.ports.name的名字
        httpHeaders:                #请求头
        - name: Custom-Header
          value: Awesome     
      tcpSocket:                    #tcp方式
        port: 8080                  #请求端口，可以使用spec.containers.ports.name的名字
      initialDelaySeconds: 5        #初始化秒数(默认0)，这里是5秒之后再开始启用存活探针
      periodSeconds: 5              #执行频率(默认10秒)   
      timeoutSeconds: 1             #探针超时后等待秒数(默认1秒)
      successThreshold: 1           #探测器在失败后，被视为成功的最小连续成功数。默认值是 1。 存活和启动探测的这个值必须是 1
      failureThreshold: 3           #当探测失败时，Kubernetes 的重试次数，(默认3次)
    readinessProbe:                 #就绪探针(检测容器是否准备就绪,保护慢容器)
      xxx: 
    startupProbe:                   #启动探针，此探针存在，其他探针禁用，直到此探针成功为止
      xxx:  
  restartPolicy: OnFailure          #容器重启策略， 取值Always(默认)、OnFailure(异常退出时重启)、Never(从不重启)
  nodeName: node-1                  #容器选择在nodeName为node-1的节点运行，如果节点名不存在，或者节点资源不够，则会报错(不建议使用)
  nodeSelector:                     #节点选择器
    disktype: ssd                   #选择节点标签有disktype: ssd的节点运行此容器
  imagePullSecrets:                 #拉取私有仓库需要登录时候，指向设置的Secrets
      - name: registry-secret       #secret的名字
  affinity:                     
    nodeAffinity:                                       #节点亲和性
      requiredDuringSchedulingIgnoredDuringExecution:   #硬亲和性
        nodeSelectorTerms:                              #节点选择器
        - matchExpressions:                             #表达式
          - key: kubernetes.io/e2e-az-name              #相当于节点标签的键
            operator: In                                #操作符有(In，NotIn，Exists，DoesNotExist，Gt，Lt)，In代表只在在下面值的其中一个就行
            values:                                     #相当于节点标签的值
            - e2e-az1
            - e2e-az2
      preferredDuringSchedulingIgnoredDuringExecution:  #软亲和性
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In                                
            values:
            - another-node-label-value
    podAffinity:                                        #pod亲和性
      requiredDuringSchedulingIgnoredDuringExecution:   #硬亲和性
      - labelSelector:                                  #标签选择器
          matchExpressions:       
          - key: security         
            operator: In                                #操作符，(In，NotIn，Exists，DoesNotExist)
            values:
            - S1
        topologyKey: topology.kubernetes.io/zone        #拓扑域，这里指节点标签的 key 必须有这个
      preferredDuringSchedulingIgnoredDuringExecution:  #软亲和性
    podAntiAffinity:                                    #pod反亲和性
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: security
              operator: In
              values:
              - S2 
          topologyKey: topology.kubernetes.io/zone     
  tolerations:                    #污点容忍
  - key: "key1"                   #污点key
    value: "value1"               #污点value
    operator: "Equal"             #策略 Equal(默认)key=value， Exists只要key符合就行
    effect: "NoSchedule"          #污点类型 NoSchedule,NoExecute,PreferNoSchedule
    tolerationSeconds: 100        #多久被驱逐，只有effect为NoExecute有效
  priorityClassName: h-priority   #优先级准入器，定义pod是否抢占      
```


#### pod生命周期

* Pending
* Running：pod内容器都被创建，并且至少一个容器已经运行或处于启动和重启阶段
* Succeeded：pod内所有容器都成功终止，并且不会重启
* Failed（失败）：pod内所有容器都终止，并且至少一个容器是失败终止
* Unknown：无法获得pod状态

**如果node挂掉或者与集群失联，则node上所有pod都会被设置为 Failed**

#### pod内容器的生命周期

* Waiting：例如正在拉取镜像等，可以通过 kubectl 查看 pod 的 Reason 字段
* Running
* Terminated: 终止，容器正常结束或者异常终止



#### 镜像拉取策略

.spec.containers.imagePullPolicy

* IfNotPresent：如果不存在则拉取
* Always：每次都拉取
* Never：从不拉取，如果节点没有此镜像，则此容器启动失败

建议指定容器版本(标签)，或者摘要，例如 image@v2.24 或者 image@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf

几种情况下的省略 imagePullPolicy
* 容器镜像指定了摘要，则自动设置为 IfNotPresent
* 容器镜像指定了非 latest 的版本，则自动设置为 IfNotPresent
* 容器镜像指定了 latest 的版本，则自动设置为 Always
* 容器镜像没有指定版本和摘要，则自动设置为 Always

#### pod内容器

* infra容器(k8s.gcr.io/pause)
* init容器
* 临时容器
* 应用容器(我们的业务容器)

pod内容器启动顺序

```
pause容器(启动完处于pause) --> init容器(可选) --> 应用容器(单个或多个超亲密关系的容器)
```

##### pause容器

* 每个pod中都有一个**k8s.gcr.io/pause**容器，在创建pod时候启动，并处于pause状态
* pod的健康检查会检查此容器
* pod的network，volumes都是此容器

##### init容器

* init容器在应用容器前启动
* 如果有多个init容器，所有init容器全都运行成功后才会去启动应用容器
* 多个init容器，会逐个按顺序启动，当一个init容器启动成功后，才会去启动下一个，而应用容器则没有此约束

##### 临时容器

##### 应用容器

修改 Pod 模版（yaml文件）或者切换到新的 Pod 模版都不会对已经存在的 Pod 起作用。 Pod 不会直接收到模版的更新。相反， 新的 Pod 会被创建出来，与更改后的 Pod 模版匹配。


#### 容器探针

* 三种探针类型
  * livenessProbe(存活探针)
  * readinessProbe(就绪探针)
  * startupProbe(启动探针)
* 三种探针检测方式
  * exec
  * httpGet
  * tcpSocket
* 三种探针结果
  * Success（成功）：容器通过了诊断。
  * Failure（失败）：容器未通过诊断。
  * Unknown（未知）：诊断失败，因此不会采取任何行动


#### 调度策略

* nodeName(节点名)：直接指定node节点，不经过调度
* nodeSelector(节点选择器)：在有此标签的节点上运行
* affinity.nodeAffinity(节点亲和性)
* affinity.podAffinity(pod亲和性)
* affinity.podAntiAffinity(pod反亲和性)
* tolerations(污点容忍)

**节点选择和节点亲和性**
1. 如果存在nodeName，则只看nodeName，优先级最高
2. 如果 nodeSelector 和 nodeAffinity都存在，两者必须都要满足， 才能将 Pod 调度到候选节点上。
3. 如果 nodeAffinity 类型下有个多个 nodeSelectorTerms，则只要一个 nodeSelectorTerms 满足的话，pod将可以调度到节点上。
4. 如果 nodeSelectorTerms 下有多个 matchExpressions，则需要所有 matchExpressions 都满足
5. 只在调度期间有效，后期修改了节点标签，pod不会被删除


**pod亲和性和反亲和性**

1. 对于 pod亲和性 和 pod反亲和性的硬亲和下 topologyKey 不允许为空。
2. 对于 pod反亲和性的硬亲和下， 准入控制器 LimitPodHardAntiAffinityTopology 被引入来限制 topologyKey 不为 kubernetes.io/hostname
3. 对于 pod反亲和性的软亲和下，topologyKey 为空意为所有(kubernetes.io/hostname，topology.kubernetes.io/zone，topology.kubernetes.io/region)
4. 除上述情况外，topologyKey 可以是任何合法的标签键。




