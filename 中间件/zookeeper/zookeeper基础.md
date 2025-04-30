## zookeeper

一个leader，多个flower 和 observer
ZooKeeper 是有序的


分层命名空间
```
/
    /zookeeper
    /znode1
        /znode1/leaf1
        /znode1/leaf2
    /znode2
```


#### znode
ZooKeeper 命名空间中的每个节点都可以拥有与其关联的数据以及子节点。这就像拥有一个允许文件同时作为目录的文件系统。
每个节点 做一个 ZNode 每个节点默认能存储1MB数据

即每个节点既能存一个节点名也能存数据


ZooKeeper 非常快，也非常简单。但由于它的目标是成为构建更复杂服务（如同步）的基础，因此它提供了一组保证。这些保证包括：

* 顺序一致性 - 客户端的更新将按照发送的顺序应用。
* 原子性 - 更新要么成功，要么失败。没有部分结果。
* 单一系统映像 - 无论客户端连接到哪个服务器，它都会看到相同的服务视图。
* 可靠性 - 一旦应用了更新，它将从那时起持续存在，直到客户端覆盖该更新。
* 及时性 - 保证客户对系统的视图在一定时间范围内是最新的。

#### znode类型


* **持久节点（Persistent znode）**：创建后不会因为客户端的断开连接而消失，只有明确的删除操作才能删除持久节点。
```sh
create [PATH]
```


* **顺序节点（Sequential znode）**：在节点路径的末尾添加一串递增的数字来创建顺序节点，确保节点在同一父节点下按照创建顺序排列。
```sh
create -s [PATH]
```


* **临时节点（Ephemeral znode）**：与客户端会话绑定的节点，当客户端会话结束（例如客户端断开连接）时，临时节点会自动删除。
```sh
create -e [PATH]
```


* **临时顺序节点（Ephemeral Sequential znode）**：结合了临时节点和顺序节点的特性，节点会在客户端断开连接时自动删除，并且节点名称末尾会添加递增的序列号。
```sh
create -e -s [PATH]
```


#### API：非常简单，只有这几种

* create : 创建节点
* delete : 删除节点
* exists : 判断节点是否存在
* get data : 从节点读数据
* set data : 写数据到节点
* get children : 获取子节点列表
* sync : waits for data to be propagated







#### 状态

通过 ls -s [PATH] 来查看的内容
```
cZxid = 0x100000002                     #创建此znode的zxid
ctime = Wed Jul 03 15:20:55 CST 2024    #创建时间
mZxid = 0x100000002                     #最后修改此节点的zxid
mtime = Wed Jul 03 15:20:55 CST 2024    #修改时间
pZxid = 0x100000007                     #最后修改子节点的zxid
cversion = 4                            #子节点的更改次数
dataVersion = 0                         #
aclVersion = 0                          #znode ACL 的更改次数
ephemeralOwner = 0x0                    #如果是临时节点，则为会话者ID，不是临时节点为0
dataLength = 8                          #此节点数据长度
numChildren = 2                         #子节点数量
```


#### zxid

ZXID（Zookeeper Transaction ID）是一个全局递增的事务ID，用于标识每一个事务操作（写操作）。它保证了所有事务操作的顺序一致性。ZXID是64位的整数

ZXID由两个部分组成：
* **epoch**（纪元）：高32位：每次选举出新的Leader时，Leader会增加自己的epoch值。这个值表示Leader的任期，确保新的Leader任期内的事务ZXID都比之前的任期高。
* **counter**（计数器）：低32位：在同一Leader任期内，每次生成新的事务Proposal时，计数器递增，从而保证每个事务ZXID的唯一性和顺序性。




#### ACL


* ACL 不是递归的。例如：/app仅可由 ip:x.x.x.x 读取，而/app/status可供所有人读取



当客户端连接到 ZooKeeper 并验证自身身份时，ZooKeeper 会将与客户端对应的所有 ID 与客户端连接关联起来。当客户端尝试访问节点时，会根据 znode 的 ACL 检查这些 ID。ACL 由(scheme:expression, perms)对组成。表达式的格式特定于方案。例如，(ip:19.22.0.0/16, READ)对向 IP 地址以 19.22 开头的任何客户端授予READ权限。


* 权限类型
  * c、CREATE
  * r、READ
  * w、WRITE
  * d、DELETE
  * a、ADMIN：可以设置权限


* 身份验证机制
  * world：有一个唯一的 id：**anyone**，代表任何人
  * auth
  * digest
  * ip：基于客户端 IP 地址进行访问控制
    * 例如：ip:192.168.1.1:crwda
  * x509
