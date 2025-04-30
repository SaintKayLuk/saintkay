## 卷

kubernetes可以和docker一样直接使用卷挂载

* 卷类型
  * emptyDir
  * hostPath
  * local
  * nfs


### emptyDir

1. 默认为空，随pod创建而创建，随pod删除而删除
2. 同一个pod内多个容器可以共享 emptyDir 卷内的内容


yaml示例
```yaml
apiVersion: v1                    
kind: Pod  
metadata:                       
  name: test-pod                  
spec:
  containers:               
  - name: nginx             #一个nginx容器   
    image: nginx
    volumeMounts:
    - mountPath: /tmp       #nginx容器内的 /tmp 目录挂载
      name: test-volume
  - name: tomcat            #一个tomcat容器
    image: tomcat
    volumeMounts:
    - mountPath: /tmp       #tomcat容器内的 /tmp 目录挂载
      name: test-volume
  volumes:
  - name: test-volume
    emptyDir: {}
  #  emptyDir:
  #    medium: Memory       #指定内存存储
```


### hostPath

和docker一样，直接映射节点目录文件
因为每个节点不同，一般需要自己手动指定节点

yaml示例
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: xxx
    name: xxx
    volumeMounts:
    - mountPath: /test-pd       # 容器内路径
      name: test-volume         # volume名字，当多个volumes时候，对应其中一个，如果没有找到则报错
  volumes:
  - name: test-volume
    hostPath:
      path: /data               # 宿主上目录位置
      type: Directory           # 卷类型，(可选，默认空字符串)
```


| type               | 行为                                                                                                         |
|--------------------|------------------------------------------------------------------------------------------------------------|
| 空字符串(默认不写) | 安装 hostPath 卷之前不会执行任何检查                                                                         |
| DirectoryOrCreate  | 如果在给定路径上什么都不存在，那么将根据需要创建空目录，可以创建多级目录，权限设置为 0755，具有与 kubelet 相同的组和属主信息。     |
| Directory          | 在给定路径上必须存在的目录。                                                                                   |
| FileOrCreate       | 如果在给定路径上什么都不存在，那么将在那里根据需要创建空文件，权限设置为 0644，具有与 kubelet 相同的组和所有权。 |
| File               | 在给定路径上必须存在的文件。                                                                                  |



