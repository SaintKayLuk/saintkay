
1. 删除pod不会删除pvc
2. 删除pvc会等待使用此pvc的pod删除之后才会被删除
3. 删除pv会等待绑定到此pv的pvc删除之后才会被删除
4. 删除pvc会根据pv的回收策略来删除pv和存储数据
5. pod可以挂载多个pvc
6. pvc可以被多个pod同时使用
7. pvc和pv一对一绑定

```
pod --> pvc --> pv --> 实际存储
```

## PersistentVolume

1. PV 是集群资源， 事先创建 或 使用 Storage Class 动态创建
2. PVC 是 Pod 对存储的请求。和Pod类似， Pod 会耗用节点资源，而 PVC 会耗用 PV 资源
3. 删除被某 Pod 使用的 PVC 对象时，该 PVC 不会被立即删除。直到不被任何 Pod 使用 
4. 删除已绑定到某 PVC 的 PV ，该 PV 不会立即删除。 直到该 PV 不再绑定到 PVC
5. PV 和 PVC 的绑定是一对一关系，即一个PVC 绑定一个PV


* pv 供应方式
    * 静态供应：事先创建好pv，再使用
    * 动态供应：基于 Storage Class 来实现，集群必须已经创建并配置了 Storage Class


yaml示例
```yaml
apiVersion: v1                  #api版本     
kind: PersistentVolume          #定义资源类型为PV
metadata:
  name: pv0003                  #资源名
spec:
  capacity:                     
    storage: 5Gi                          #存储容量，单位可以是Gi和Ti等
  volumeMode: Filesystem                  #卷模式：Filesystem(文件系统) 和 Block(块)。默认为 Filesystem
  accessModes:                            #定义pv的访问模式
    - ReadWriteOnce                       #卷可以被一个节点以读写方式挂载
    - ReadOnlyMany                        #卷可以被多个节点以只读方式挂载
    - ReadWriteMany                       #卷可以被多个节点以读写方式挂载
  persistentVolumeReclaimPolicy: Recycle  #回收策略，Retain，Recycle，Delete 
  storageClassName: slow                  #存储类，特定存储类只能绑定到指明该存储类的pvc，没有存储类的pv绑定到没有存储类的pvc
  mountOptions:                           #挂载选项
    - hard
    - nfsvers=4.1
  nfs:                          #卷插件，这里
    path: /tmp
    server: 172.17.0.2
```


#### volumeMode(卷模式)

* Filesystem： 会被 Pod 挂载（Mount） 到某个目录。如果卷的存储来自某块设备而该设备目前为空，Kuberneretes 会在第一次挂载卷之前 在设备上创建文件系统。
* Block：作为原始块设备来使用，pod和卷之间不存在文件系统层，pod中运行的应用需要能够处理原始块设备


#### accessModes(访问模式)

每个卷可以支持多种访问模式，但是只能同一时刻只能以一种访问模式挂载
例如 pv被多个pod以只读模式挂载，则不能再让其他pod以读写方式挂载

#### 回收策略

1. 删除挂载pvc的pod不会删除pvc
2. 而删除pvc时，pv根据回收策略来决定pv的去留

* Retain： 保留，手动回收，即删除pvc，pv会被保留，即使删除pv，卷上存储的数据也还存在
* Recycle：回收，会在卷上执行一些基本的擦除 （rm -rf /thevolume/*）操作，之后允许该卷用于新的 PVC 申领。
* Delete：删除，删除pvc会删除绑定的pv，并且卷上的数据也会被删除


**Retain**

1. 删除pvc时，绑定的pv会一直处于 Released 状态
2. 编辑pv，删除 spec.claimRef 的内容，让 pv 重新成为  Available
    ```
    kubectl edit pv [pvName]
    ```
3. pv中数据保留，不会被删除

**Recycle**

1. 删除pvc后，绑定的pv会重新变成 Available
2. 删除pvc后，绑定的pv会删除pv内的数据，(例如执行 rm -rf /* 的操作)

需要卷类型支持 Recycle插件
目前，仅 nfs 和 hostPath 类型支持 Recycle

**Delete**

1. 删除pvc后，会删除绑定的pv
2. 并且删除 pv 对应的远程存储内存

需要卷类型支持 Delete 插件

#### pv状态

pv的状态

* Available ：卷是一个空闲资源，尚未绑定到任何申领；
* Bound ：该卷已经绑定到某申领；
* Released ：所绑定的pvc已被删除，但是资源尚未被集群回收
* Failed ：卷的自动回收操作失败
* Terminating ：已执行pv的删除操作，但是还绑定着pvc，删除pvc后则会删除此pv

## PersistentVolumeClaims

pvc的作用
1. 给pod使用
2. 绑定pv

pvc的存储限制
1. pvc的存储限制，取决于绑定的pv的存储大小，最终取决于底层存储类型(TODO 这里需要改进)
   例如nfs就限制不了存储，pv的请求是5G，pvc的请求是3G，但是实际可以存储5G以上
2. 受限于 LimitRange 的限制 


yaml示例
```yaml
apiVersion: v1                #api版本
kind: PersistentVolumeClaim   #资源类型为pvc
metadata:
  name: myclaim               #pvc的名字
spec:
  accessModes:                #访问模式，需要支持此访问模式的pv
    - ReadWriteOnce
  volumeMode: Filesystem      #卷类型，需要和pv对应
  resources:                  #请求的资源
    requests:
      storage: 8Gi            #请求8个G的存储资源
  storageClassName: slow      #存储类，通过存储类来指定需要绑定的pv(pv拥有相同的存储类)
  selector:                   #标签选择器
    matchLabels:              #pv必须包含此 标签
      release: "stable"
    matchExpressions:         #通过 key，values 和 operator 来决定，operator有 In、NotIn、Exists 和 DoesNotExist
      - {key: environment, operator: In, values: [dev]}
```

pv 绑定 pvc ，需要：
1. 符合存储类，如果pvc指定了 storageClassName ，则需要同样storageClassName的pv，如果pvc没有指定storageClassName，则绑定没有 storageClassName 的pv
2. 符合标签选择器，selector 下的所有条件都满足
3. 访问模式支持
4. 卷类型相同
5. 请求的资源足够，例如pvc需要 8G 资源，则只要要有 8G 以上资源的 PV，可以绑定大于8G存储的pv，但是不能绑定小于8G存储的pv







