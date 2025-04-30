


PriorityClass示例
```yaml
apiVersion: scheduling.k8s.io/v1        #指定api版本
kind: PriorityClass                     #指定资源类型
description: "描述信息"
metadata:
  name: high-priority                   #名字
value: 100000                           #
globalDefault: false                    #只能设置一个priorityclass为true，未指定pc的pod使用此pc
PreemptionPolicy: PreemptLowerPriority  #优先策略。可选 PreemptLowerPriority(默认) 和 Never
```


系统中只能存在一个 globalDefault 设置为 true 的 PriorityClass。 如果不存在设置了 globalDefault 的 PriorityClass， 则没有 priorityClassName 的 Pod 的优先级为零。


