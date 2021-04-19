raft是一种强一致性、去中心化、高可用的分布式协议

raft算法是一种`共识性算法`，即需要大多数节点就某件事情达成一致

[参考1](https://www.cnblogs.com/xybaby/p/10124083.html)

[参考2](https://zhuanlan.zhihu.com/p/347451492)

[演示动画](http://thesecretlivesofdata.com/raft/)

## raft的工作原理

选举leader，由leader负责管理replicated log，leader接收客户端请求，并将请求复制到follower，如果leader产生故障，由follower选举出新的leader

raft有两个重要的子问题：leader election和log replication

### leader election

raft算法中节点有三种状态：`leader`，`follower`和`candidate`，每个节点在任意时刻处于三种状态之一

- 1.最开始都是`follower`状态，当一段时间内没有收到`leader的心跳`，就转变成candidate

- 2.candidate节点会发起选举，首先将自己的`term加1`并`投自己一票`，然后通知其他节点自己的选举状态，由其它节点进行投票，如果某个candidate得到`超过半数`的票，它就成为新的leader，如果candidate发现已经有了leader（有`更高的term值`），就切换到follower

- 3.每个leader有一个任期`term`，任期结束会发起新的选举

#### 选举的问题

选举时有几个约束条件：

- 1.在一个任期内，单个节点只能`投一票`

- 2.`先到先得`，即会为最先收到请求的candidate投票（前提是对方的日志`不能比自己的日志旧`）

- 3.candidate必须知道比自己更多的信息（通过 log replication 实现）

如果在选举阶段两个candidate出现了平票，会在一段超时时间后重新选举，这其实带来了一定的延迟，为了避免这种情况，有两个措施：

- 1.为每个节点设置随机的选举等待时间，尽量让节点在`不同时刻`发起选举，这样根据先到先得的约束会选出最早发起选举的candidate

- 2.尽量设置节点总数为`奇数`，以避免平票

### log replication

log replication是为了保证节点的数据一致性

当leader接收到客户端的写入操作请求时，步骤如下：

- 1.leader向自己的日志添加一条记录（log entry）

- 2.leader向所有follower发起AppendEntries RPC进行`log同步`

- 3.如果收到`超过半数`follower的成功返回就将这条记录`更新到自己的状态机`，并`向客户端返回`

- 4.leader更新所有`follower的状态机`

注意在向客户端返回之前，follower只是更新了日志，并`没有更新节点状态`（比如在数据库中并没有把数据实际上写入）

### 安全性

raft通过以下几个方面来保证分布式系统的数据安全性

#### Election Safety

一个任期内最多有一个leader被选出（出现多个leader称为`脑裂`），通过下面两点来保证：

- 1.一个节点在一个任期内只能投一票

- 2.获得超过半数票的节点才能称为leader

#### Leader Append-Only

leader只能向log中`追加记录`，而不能覆盖或删除

这就保证了一旦向客户端返回结果，log就不能回滚，数据也就不会被改变

#### Log Matching

log中的条目由索引号（log index）编排，其中包含被创建时的任期号（term），如下图所示

[![coGTiD.md.jpg](https://z3.ax1x.com/2021/04/19/coGTiD.md.jpg)](https://imgtu.com/i/coGTiD)

日志同步时需要保证以下两点：

- 1.如果不同的日志中两个条目有相同的索引号和任期号，则它们`存储的命令`是相同的

- 2.如果不同的日志中两个条目有相同的索引号和任期号，则它们`之前的所有条目`都是相同的

因为leader在每个位置只创建一条log entry，并且是append-only，而且在发送时会包含最新log entry的`前一个log index和term`，这样如果follower在自己的log中找不到前面那一个index和term，就会告诉leader数据不一致

如果在某个时刻leader崩溃，导致之前的旧leader没有完全复制日志条目，就可能导致`日志不一致`，比如下图的情况

[![co4cMd.md.jpg](https://z3.ax1x.com/2021/04/19/co4cMd.md.jpg)](https://imgtu.com/i/co4cMd)

此时新的leader需要找到follower和自己`日志相同的地方`，再从这个地方开始`覆盖`follower后面的日志条目

做法是`从后向前逐条尝试`，直到找到每个follower的日志一致的地方

#### Leader Completeness

如果一个日志条目在某个term内被提交，那这个条目一定会出现在更高term的leader的日志里面

#### State Machine Safety

所有节点在同一个位置（index）应该应用同样的日志