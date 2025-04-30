## SatefulSets

适用于
* 稳定的、唯一的网络标识符。
* 稳定的、持久的存储。
* 有序的、优雅的部署和缩放。
* 有序的、自动的滚动更新。



* StatefulSet 需要无头服务(Headless Service) 来负责 Pod 的网络标识，即必须创建 Headless Service

yaml示例
```yaml

```



