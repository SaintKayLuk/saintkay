## Windows Server 故障转移集群 (WSFC) 仲裁方式对比

| 仲裁模式                                               | 适用场景                    | 组成方式                               | 优点                                                    | 缺点                                                              |
| ------------------------------------------------------ | --------------------------- | -------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------- |
| **Node Majority (节点多数)**                           | 节点数为 **奇数**（≥3）     | 仅节点有投票                           | 最佳方案；无外部依赖；集群容错性强                      | 至少需要 3 节点才能使用                                           |
| **Node and File Share Majority (节点 + 文件共享多数)** | 节点数为 **偶数**（2、4 …） | 节点 + 第三方服务器上的文件共享（FSW） | 无需额外存储；FSW 不存数据，只负责投票；适合 2 节点场景 | 需要额外一台可用服务器（如域控/文件服务器）；FSW 挂掉时投票数减少 |
| **Node and Disk Majority (节点 + 磁盘见证多数)**       | 传统 SAN 存储环境           | 节点 + 共用的磁盘 LUN 作为见证         | 磁盘挂载在集群中；实现简单                              | 依赖共享存储；存储成为潜在单点故障；云环境不推荐                  |
| **No Majority (Disk Only，磁盘见证模式)**              | 特殊情况，不推荐            | 仅依赖见证磁盘                         | 节点数为偶数、必须依赖一个磁盘才能运行                  | 强烈不推荐：见证磁盘挂了=集群挂了；可用性最低                     |



📌 最佳实践

* 推荐优先级
  * 奇数节点 → Node Majority（最优）
  * 偶数节点 → Node + File Share Witness（常见于 2 节点部署）
  * Node + Disk Witness 只在有共享存储的传统环境下用，现代架构不推荐
  * Disk Only 基本淘汰，不要用

* 特别说明
  * FSW 掉线不会导致集群挂掉，只会少一个投票。真正决定集群能否继续运行的，还是“是否超过半数节点存活”。
  * 见证服务器（FSW/Disk Witness）最好放在 与集群节点不同的地方（比如 AD 域控机），避免和节点同时挂掉。




## 日志查询

导出日志到 C:\ClusterLog 不指定时间则导出所有，TimeSpan 的单位是分钟

```powershell
# 导出最近30分钟的集群日志
Get-ClusterLog -UseLocalTime -TimeSpan 30 -Destination C:\ClusterLog

# 导出最近2小时的日志
Get-ClusterLog -UseLocalTime -TimeSpan 120 -Destination C:\ClusterLog

# 只导出当前节点的日志
Get-ClusterLog -Node db01 -UseLocalTime -TimeSpan 60 -Destination C:\ClusterLog
```

搜索 failover 来查询 错误日志







