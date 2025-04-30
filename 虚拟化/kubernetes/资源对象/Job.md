# Job

用Job运行任务的三种场景
1. 非并行job
   * 通常只启动一个 Pod，除非该 Pod 失败
   * 当 Pod 成功终止时，立即视 Job 为完成状态
2. 具有确定完成计数的并行 Job
   * .spec.completions 字段设置需要完成的pod数
   * job代表整个任务，当成功的pod数量到达 .spec.completions 时，则job完成
3. 带工作队列的并行 Job
   * ...

yaml示例
```yaml
apiVersion: batch/v1        
kind: Job                   # 定义资源类型
metadata:
  name: pi
spec:
  completions: 1                # job完成次数，成功状态的 pod 到达此次数后，job任务完成，(默认值为1)
  #completionMode: NonIndexed    # 完成模式，取值为 NonIndexed(默认值) 或 Indexed ，当为 Indexed 时， Pod 会获得对应的完成索引，取值为 0 到 .spec.completions-1
  parallelism: 1                # 并行性请求，即当运行多个pod任务时，同时运行的pod数量(默认值为1)
  backoffLimit: 4               # job重试次数，超过此次数这job为失败
  activeDeadlineSeconds: 30     # job活跃时间，job最大运行时间，优先级高于backoffLimit，当job运行此时间后停止，无论job是否已经执行完
  ttlSecondsAfterFinished: 60   # 已完成 Job 的自动清理,在完成后(Complete 或 Failed) 几秒后自动清理 job
  template:                     # pod模板        
    spec:
      containers:
      - name: pi
        image: perl:5.34.0
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never      # 重启策略，只能是 Never 和 OnFailure 
```


#### 回退失败策略


.spec.backoffLimit 来设置回退失败的次数

计算重试次数的两各取值
1. 根据job的 .status.phase = "Failed" 的 Pod 数量
2. 当 Pod 的 restartPolicy = "OnFailure" 时，针对 .status.phase 等于 Pending 或 Running 的 Pod，计算其中所有容器的重试次数

当其中一个值达到 .spec.backoffLimit 时，这此 job 被判定为 失败

#### job的终止和清理

.sepc.activeDeadlineSeconds
当job运行到 .sepc.activeDeadlineSeconds 设置的时间后，job会停止，不管job是否执行完

.sepc.ttlSecondsAfterFinished
当job终止后，等待 .sepc.ttlSecondsAfterFinished 秒后，删除job
