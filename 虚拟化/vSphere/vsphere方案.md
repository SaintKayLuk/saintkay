| 条件                     | 说明                     |
| ---------------------- | ---------------------- |
| 🧠 安装 vCenter Server   | 用于集中管理多个 ESXi 主机，核心控制台 |
| 🖥 至少 2 台以上的 ESXi 主机   | 构建集群环境                 |
| 📦 共享存储（NAS/SAN）或 vSAN | 所有 ESXi 能访问同一份虚拟机磁盘    |
| 📡 配置 vMotion 网络       | 专用网络用于热迁移              |
| 🔄 启用 HA 或 vMotion 功能  | 让虚拟机能在节点间移动或接管         |



✅ 方案二：使用软件定义存储 vSAN（VMware 自家的）
VMware vSAN 是内嵌在 vSphere 里的共享存储方案

特点	内容
📦 利用每台 ESXi 上的本地硬盘组成集群存储	
📌 无需外部 NAS/SAN	
🧠 管理集成在 vCenter 里	
💰 需要额外的 vSAN License（贵！）	

构建方式：
至少3台 ESXi 主机

每台必须有至少一块 SSD（缓存盘）+ HDD（容量盘）

在 vCenter 中启用 vSAN，自动聚合为一个共享 Datastore

✅ 稳定、性能好，官方强推，适合你预算充足的情况。


```
 ESXi-1     ESXi-2     ESXi-3
  |           |          |
[SSD+HDD]  [SSD+HDD]  [SSD+HDD]
     \        |        /
       \____vSAN Cluster____/
             |
     vSAN Datastore（共享）
             |
        所有虚拟机磁盘文件
```




---
🧠 推荐主流方案（性价比高）：
✅ vCenter HA（VCHA）——官方高可用方案
将 vCenter Appliance（VCSA）复制出两个副本：
Active（主） + Passive（备） + Witness（见证）




```
       [ ESXi-1 ]         [ ESXi-2 ]          [ ESXi-3 ]
        |                   |                    |
    +--------+         +--------+           +----------+
    | Active | <-----> | Passive| <-------->| Witness  |
    +--------+         +--------+           +----------+
             \                             /
              \------ Heartbeat ---------/
```


真正高可用、不中断	使用 VCSA + vCenter HA 架构（VCHA）

