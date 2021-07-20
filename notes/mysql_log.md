mysql的日志共有6大种：错误日志，二进制日志，事务日志，慢查询日志，查询日志和中继日志

[参考](https://segmentfault.com/a/1190000023827696)

## 错误日志 Error log

文件名`*.err`

错误日志包含mysql服务器启动和关闭时的信息，以及服务器运行中的错误信息

## 事务日志

事务日志是innodb独有的日志，包括重做日志redo log和回滚日志undo log

### redo log

重做日志

文件名`*.ib_logfile`

在修改数据时，会先在内存和redo log中进行操作

redo log只记录对数据页做了哪些修改，所以它的`体积更小`，每次刷写不用对整个页操作，而且是`顺序IO`

#### 刷盘策略

redo log的刷盘有三个级别：mysql内部的`redo log buffer`，磁盘的`page cache`和`磁盘`

innodb有一个后台线程，`每秒钟一次`调用write将redo log buffer写入page cache，然后调用fsync持久化到磁盘

通过`innodb_flush_log_at_trx_commit`参数来控制，有三种情况：

- 1.值为0，每次事务提交只把redo log写到`redo log buffer`（延迟写）

- 2.值为1，每次事务提交都把redo log直接持久化到`磁盘`（实时写，实时刷）

- 3.值为2，每次事务提交只把redo log写到`page cache`（实时写，延迟刷）

#### 组提交

redo log之所以能提高IO性能，一个是因为它是顺序写，二是它可以采用组提交的方式，`一次性写入多个事务`

### undo log

回滚日志

文件名`*.ibdata`

每次修改数据`之前`，都要将对应的恢复操作写入undo log

undo log是逻辑日志，记录的是与当前操作相反的操作，如执行insert，就记录一条delete

## 二进制日志 binlog

记录所有修改数据库的操作，以及消耗的资源

主要在`备份`和`主从复制`场景中应用

二进制日志对所有操作进行记录，所以会影响性能，默认是`关闭的`

执行流程：

- 1.事务执行过程中，把日志写到binlog cache

- 2.事务提交时，把binlog cache写到binlog文件中

一个事务的binlog必须`一次性写入`，如果事务很大，超过了binlog cache的范围，就要暂存到磁盘

### binlog的模式

可以通过下面的语句来查看：

```
show global variables like '%binlog_format%'
```

- Row Level

行模式，日志中会记录每一行数据被修改的形式，如果有slave端，就在slave端对相同的数据进行修改

优点：不需要记录sql语句的上下文信息，只需要记录`哪一条`被修改

缺点：每一行的修改都被记录，产生`大量日志内容`（删除10万条数据就有10万条日志记录）

- Statement Level（默认）

语句模式，将每一条修改数据的`sql语句`记录到binlog中，如果有salve端，它的sql线程会解析成与master端执行过的相同sql语句来执行

优点：只记录执行的语句，而不是具体被修改的数据，日志量较少（删除10万条数据可能只需要一个语句）

缺点：由于只记录语句，有时复制会出现错误，比如使用某些`函数`的时候

- Mixed

自动模式，会根据执行的具体sql语句来自动选择Row或Statement模式

### 刷盘策略

通过`sync_binlog`参数来配置刷写策略，有两种情况：

- 1.值为`0`，每次提交事务都只write到page cache中，然后依赖操作系统来刷写binlog，而不是mysql主动操作

- 2.值为`N(N>0)`，每次提交事务都write，每`写N次`page cache，就调用一次`fdatasync()`进行刷写

## 慢查询日志 Slow query log

文件名`hostname-slow.log`

记录执行时间较长的操作（不仅仅是select）

默认是关闭的

## 查询日志 Query log

文件名`hostname.log`

记录所有执行的query

默认是关闭的

## 中继日志 Relay log

在主从复制中，从服务器复制主服务器的`二进制文件`到从服务器的中继日志（IO线程），然后`重放`日志中的事件（SQL线程）

## 日志刷写到磁盘的策略

主要通过两个参数`innodb_flush_log_at_trx_commit`（redolog）和`sync_binlog`（binlog）两个参数来配置刷写策略

对于redolog，innodb_flush_log_at_trx_commit的配置有三种：

- 1.值为`0`，log buffer`每秒一次`写入log file中，并且log file的`刷写操作（flush）同时进行`

- 2.值为`1`，每次`事务提交`时把log buffer写入log file，并`同时flush`

- 3.值为`2`，每次`事务提交`时把log buffer写入log file，但不同时flush，而是`每秒flush一次`

对于binlog，sync_binlog有两种策略：

- 1.值为`0`，依赖操作系统来刷写binlog，而不是mysql主动操作

- 2.值为`N(N>0)`，每`写N次`binlog，就调用一次`fdatasync()`进行刷写

## 日志的执行顺序

ubdo log, redo log与binlog的写入顺序如下图所示

要注意redo log的`两阶段提交`，commit之后redo log才是可用的，在commit之前，如果binlog已经写入，则可以根据binlog恢复数据


图中黄色表示在执行器中执行的操作，白色表示在存储引擎中执行的操作

[![WmSE11.png](https://z3.ax1x.com/2021/07/15/WmSE11.png)](https://imgtu.com/i/WmSE11)

redo log与binlog有共同的字段`XID`，可以根据它来确定同一条日志