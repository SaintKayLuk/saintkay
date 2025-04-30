# CronJob

基于时间重复调用job

cronjob 管理job，job管理pod，类似于deployment
pod <-- job <-- cronjob

yaml示例
```yaml
apiVersion: batch/v1            #根据kubenetes版本不同，通过kubectl api-resources 来查看
kind: CronJob                   #资源类型
metadata:
  name: hello
spec:
  schedule: "* * * * *"         # cron语法
  concurrencyPolicy: Allow      # 并发性规则，可选 Allow(默认)、Forbid、Replace
  startingDeadlineSeconds: 60   # 如果错过了调度时间，则会在设置的时间内执行，如果超过此时间，则不执行
  jobTemplate:                  # job模板
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox:1.28
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

cron语法
```sh
# ┌───────────── 分钟 (0 - 59)
# │ ┌───────────── 小时 (0 - 23)
# │ │ ┌───────────── 月的某天 (1 - 31)
# │ │ │ ┌───────────── 月份 (1 - 12)
# │ │ │ │ ┌───────────── 周的某天 (0 - 6)（周日到周一；在某些系统上，7 也是星期日）或者是 sun，mon，tue，web，thu，fri，sat
# │ │ │ │ │
# │ │ │ │ │
# * * * * *
```


#### 并发性规则

.spec.concurrencyPolicy

* Allow：允许并发任务执行
* Forbid：不允许并发任务执行，如果新任务的执行时间到了而老任务没有执行完，则忽略新任务执行
* Replace：不允许并发任务执行，如果新任务的执行时间到了而老任务没有执行完，则新任务替换旧任务


