## 事务的ACID特性

- Atomicity（原子性），事务本身不可拆分，要么全部提交，要么全部回滚

- Consistency（一致性），数据库总是从一个一致的状态转变到另一个一致的状态，未提交的事务所做的修改不会到达数据库

- Isolation（隔离性），事务未提交之前所做的修改对其他事务不可见

- Durability（持续性），事务所做的更改是永久更改

### 如何保证ACID

#### 原子性

通过innodb的`undo log`回滚日志来保证，undo log存储了`恢复数据`需要的信息

#### 一致性

数据库通过AID三个特性来保证C

#### 隔离性

利用锁和MVCC（多版本并发控制）

#### 持久性

通过innodb的`redo log`重做日志，它记录了数据库中`页`的修改

redo log包括两部分：`内存中`的redo log buffer（易失性）和`磁盘上`的redo log file（持久性）

在数据准备修改前，要先将修改写入redo log中

因此即使断电，未完成的数据修改也不会丢失

## 事务的隔离级别

[参考](https://developer.aliyun.com/article/746718)

有四个隔离级别

### 1.读未提交 Read Uncommited

事务A在未提交之前可以读取事务B还没提交的更改，导致`脏读`

[![6UpcNj.png](https://s3.ax1x.com/2021/03/12/6UpcNj.png)](https://imgtu.com/i/6UpcNj)

### 2.读已提交 Read Commited

事务`A在未提交之前`可以`读取事务B已提交`的内容

[![6Upfg0.png](https://s3.ax1x.com/2021/03/12/6Upfg0.png)](https://imgtu.com/i/6Upfg0)

也叫不可重复读，是大多数数据库的默认隔离级别，但不是MySQL的

### 3.可重复读 Repeatable Read

事务`A在未提交之前`，无法看到其他事务的更改，无论其他事务是否提交

是MySQL的`默认`隔离级别

[![6UphvV.png](https://s3.ax1x.com/2021/03/12/6UphvV.png)](https://imgtu.com/i/6UphvV)

可能导致`幻读`，如图中虚线部分所示，查询时找不到，插入又插入不了，就像出现了幻觉

### 4.可串行化 Serializable

在读取时`加锁`，所有事务串行执行，保证了安全性，但效率很低，因为要竞争