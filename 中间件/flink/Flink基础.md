
## flink组件

一个flink集群包括 一个JobManager 和 一个或多个 TaskManager

* Flink Client
    * 命令行界面
    * REST 端点
    * SQL 客户端 
* JobManager
    * JobMaster：负责管理单个JobGraph的执行，每个作业都有自己的 JobMaster
    * ResourceManager：负责 Flink 集群中的资源提供、回收、分配。它管理 task slots
    * Dispatcher：
        1. 提供了一个 REST 接口，用来提交 Flink 应用程序执行，并为每个提交的作业启动一个新的 JobMaster
        2. 还运行 Flink WebUI 用来提供作业执行信息
* TaskManager：worker，一个TaskManager就是一个jvm进程，一般来说一台机子几个TaskManager
    * task slot 的数量表示并发处理 task 的数量   





## flink集群


flink集群三种模式

* 应用模式(Flink Application 集群)：专门为一个应用运行集群。作业的主要方法（或客户端）在 JobManager 上执行
    * 集群生命周期：仅从 Flink 应用程序执行作业
    * 资源隔离：ResourceManager 和 Dispatcher 作用于单个的 Flink 应用程序
* Per-Job Mode(Flink Job 集群)：专门为一项作业运行集群。作业的主要方法（或客户端）仅在集群创建之前运行。
    * 集群生命周期：
    * 资源隔离：JobManager 中的致命错误仅影响在 Flink Job 集群中运行的一个作业。
    * 其他注意事项：由于 ResourceManager 必须应用并等待外部资源管理组件来启动 TaskManager 进程和分配资源，因此 Flink Job 集群更适合长期运行、具有高稳定性要求且对较长的启动时间不敏感的大型作业。
* 会话模式(Flink Session 集群)：一个 JobManager 实例管理共享同一个 TaskManager 集群的多个作业
    * 集群生命周期：
    * 资源隔离：
        1. 如果 TaskManager 崩溃，则在此 TaskManager 上运行 task 的所有作业都将失败
        2. 如果 JobManager 上发生一些致命错误，它将影响集群中正在运行的所有作业。
    * 其他注意事项：


**Kubernetes 不支持 Flink Job 集群**








<!-- insert into 外表，在定义主键的情况下，会触发upset，有主键记录更新，没有主键记录新增 -->




