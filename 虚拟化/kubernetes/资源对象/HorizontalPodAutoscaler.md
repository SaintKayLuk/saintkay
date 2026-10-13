# hpa


水平自动扩缩pod，针对Deployment 或者 StatefulSet

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
    scaleDown:                # 缩容策略，默认允许缩减到 minReplicas 数量的 Pod， 具有 300 秒的稳定窗口
    scaleUp:                  # 扩容策略
```