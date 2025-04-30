# ZAB算法

借鉴了Paxos算法

专为zookeeper使用

* 消息广播
* 崩溃恢复
  * Leader选举
  * 数据恢复
    


消息广播：
所有的写请求都由 leader 来处理。正常工作状态下，leader 接收请求并通过广播协议来处理。

崩溃恢复：
当服务初次启动，或者 leader 节点挂了，系统就会进入恢复模式，直到选出了有合法数量 follower 的新 leader，然后新 leader 负责将整个系统同步到最新状态。


<!-- 
Leader 服务器与每一个 Follower 服务器之间都维护了一个单独的 FIFO 消息队列进行收发消息，使用队列消息可以做到异步解耦。 Leader 和 Follower 之间只需要往队列中发消息即可。 -->


## 三种角色

* **Leader**：负责处理所有的写请求（事务请求），生成Proposal，并将Proposal广播给所有Follower和Observer节点。Leader还负责发起和管理选举过程。
* **Follower**：接收Leader的Proposal，记录Proposal，并发送ACK给Leader。在收到过半数ACK后，Leader提交事务，Follower在接收到Commit消息后，应用事务。Follower还处理读请求，并在Leader不可用时参与选举。
* **Observer**：接收Leader的Proposal，并应用事务更新，但不发送ACK给Leader，不参与选举。Observer主要用于处理读请求，以提高系统的读扩展性和性能。




## 消息广播

1. 客户端向Leader发送事务请求。
2. Leader接收到客户端的写请求后，生成Proposal
3. Leader将Proposal广播给所有Follower和Observer节点。
4. Follower接收到Proposal并记录日志，然后发送ACK给Leader。
5. Observer接收到Proposal后，记录日志（预写日志），但不发送ACK给Leader。
6. Leader接收到过半数ACK后，将Proposal应用到本地并广播Commit消息。
7. Follower和Observer接收到Commit消息后，将Proposal应用到本地数据存储中。





## 崩溃恢复

```
选举 --> 数据同步 --> 消息广播 -->
```

下面的几种情况都会进入崩溃恢复阶段：
* 初始化集群，刚刚启动的时候，无主
* Leader崩溃，因为故障宕机
* Leader失去了半数的机器支持，与集群中超过一半的节点断连，比如：发生了网络分区



Zab协议需要保证选举出来的Leader需要满足以下条件：
* 新选举出来的 Leader 不能包含未提交的 Proposal。即新选举的 Leader 必须都是已经提交了 Proposal 的 Follower 服务器节点。
* 新选举的 Leader 节点中含有最大的 zxid 。

这样做的好处是可以避免 Leader 服务器检查 Proposal 的提交和丢弃工作。


### 选举阶段

1. 初始化投票：
每个节点在启动时，首先将自己的投票初始化为自身，并发送给所有其他节点。

2. 接收投票并更新：
节点接收到其他节点的投票后，会比较它们的ZXID和myid。如果接收到的投票的ZXID更大，或ZXID相同但myid更大，节点会更新自己的投票。

3. 投票统计：
每个节点维护一个投票计数器，用于记录每个节点收到的投票数。当某个节点的投票数超过半数时，节点将该节点选为Leader。

4. Leader广播确认：
被选中的Leader会广播一个确认消息，所有节点收到确认消息后，进入同步状态

### 数据同步阶段

Leader节点根据Follower节点的ZXID，决定如何进行数据同步：

* 事务日志同步：如果Follower节点的ZXID落后于Leader，但仍在事务日志的范围内，Leader只需要发送缺失的事务日志给Follower。
* 快照同步：如果Follower节点的ZXID与Leader的差距较大，超过了Leader的事务日志范围，Leader需要发送一个快照（snapshot）来更新Follower的状态。

**事务日志同步**
对于需要同步事务日志的Follower节点，Leader会执行以下步骤：
1. 从自身的事务日志中提取出Follower缺失的日志条目。
2. 将这些日志条目按顺序发送给Follower。
3. Follower接收到日志条目后，按顺序应用这些日志，更新自己的状态。

**快照同步**
对于需要同步快照的Follower节点，Leader会执行以下步骤：

1. 生成当前状态的快照数据。
2. 将快照数据发送给Follower。
3. Follower接收到快照数据后，清空自身的事务日志和状态，并应用快照数据。


在完成事务日志或快照同步后，Follower节点会发送确认消息给Leader，表示其状态已经更新到最新。Leader收到所有Follower节点的确认消息后，才会进入正常的消息广播阶段。



## 案例

#### 问题描述
**leader发送commit之前挂了**
当 leader 收到合法数量 follower 的 ACKs 后，就向各个 follower 广播 COMMIT 命令，同时也会在本地执行 COMMIT 并向连接的客户端返回「成功」。但是如果在各个 follower 在收到COMMIT 命令前 leader 就挂了，导致剩下的服务器并没有执行都这条消息。

#### 解决方式
选举拥有 proposal 最大值（即 zxid 最大） 的节点作为新的 leader。
由于所有提案被 COMMIT 之前必须有合法数量的 follower ACK，即必须有合法数量的服务器的事务日志上有该提案的 proposal，因此，zxid最大也就是数据最新的节点保存了所有被 COMMIT 消息的 proposal 状态。
新的 leader 将自己事务日志中 proposal 但未 COMMIT 的消息处理。
新的 leader 与 follower 建立先进先出的队列， 先将自身有而 follower 没有的 proposal
发送给 follower，再将这些 proposal 的 COMMIT 命令发送给 follower，以保证所有的
follower 都保存了所有的 proposal、所有的 follower 都处理了所有的消息



#### 问题描述
当 leader 接收到消息请求生成 proposal 后就挂了，其他 follower 并没有收到此 proposal，因此经过恢复模式重新选了 leader 后，这条消息是被跳过的。 此时，之前挂了的 leader 重新启动并注册成了 follower，他保留了被跳过消息的 proposal 状态，与整个系统的状态是不一致的，需要将其删除。

#### 解决方式
Zab 通过巧妙的设计 zxid 来实现这一目的。

这样设计的好处是旧的 leader 挂了后重启，它不会被选举为 leader，因为此时它的 zxid 肯定小于当前的新 leader。当旧的 leader 作为 follower 接入新的 leader 后，新的 leader 会让它将所有的拥有旧的 epoch 号的未被 COMMIT 的 proposal 清除。
