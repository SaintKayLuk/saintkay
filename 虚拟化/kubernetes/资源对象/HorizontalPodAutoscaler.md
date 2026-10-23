# hpa


水平自动扩缩pod，针对Deployment 或者 StatefulSet，需要先部署 Metrics Server

yaml示例
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
  namespace: php-namespace
spec:
  scaleTargetRef:             #（必须）指向要扩缩的目标资源
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1              # 可以缩减的副本数的下限，默认为 1 个 Pod
  maxReplicas: 10             #（必须）副本数的上限。不能小于 minReplicas
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  behavior:                   # （可选）不写则使用默认
    scaleDown:                # 缩容策略，默认允许缩减到 minReplicas 数量的 Pod， 
    scaleUp:                  # 扩容策略
```

## 伸缩判断 metrics


例：type为Resource的示例
```yaml
metrics:
- type: Resource
  resource:
    name: cpu                 # 资源名称
    target:                   # 给定指标的目标值
      type: Utilization       # 目标值计算方式
      averageUtilization: 50  # 指标百分比，目前仅对 Resource 有效
```

指标类型，选定下面值之一
* metrics.type
  * Resource：cpu、内存等资源指标
  * ContainerResource：指定容器的资源指标
  * Pods：多个pod自定义指标
  * Object：集群中某个对象指标
  * External：集群外部或外部监控提供的指标

指标的目标值计算方式，
* metrics.[type].target.type
  * Utilization：利用率，例如cpu百分比
  * AverageValue
  * Value


## 扩缩容策略 behavior

扩容和缩容都可以配置 稳定窗口、伸缩策略和策略选择方式

默认值
```yaml
behavior:                  
  scaleDown:                          # 缩容策略，默认允许缩减到 minReplicas 数量的 Pod， 
    stabilizationWindowSeconds: 300   # 具有 300 秒的稳定窗口
    policies:
    - type: Percent
      value: 100
      periodSeconds: 15
  scaleUp:                            # 扩容策略
    stabilizationWindowSeconds: 0
    policies:
    - type: Percent
      value: 100
      periodSeconds: 15
    - type: Pods
      value: 4
      periodSeconds: 15
    selectPolicy: Max
```



