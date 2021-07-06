mysql的日志共有6大种：错误日志，二进制日志，事务日志，慢查询日志，查询日志和中继日志

[参考](https://segmentfault.com/a/1190000023827696)

## 错误日志 Error log

文件名`*.err`

错误日志包含mysql服务器启动和关闭时的信息，以及服务器运行中的错误信息

## 事务日志

事务日志是innodb独有的日志，包括重做日志redo log和回滚日志undo log

- 重做日志

文件名`*.ib_logfile`

在修改数据时，会先在内存和redo log中进行操作

redo log只记录对数据页做了哪些修改，所以它的`体积更小`，每次刷写不用对整个页操作，而且是`顺序IO`

- 回滚日志

文件名`*.ibdata`

每次修改数据`之前`，都要将对应的恢复操作写入undo log

undo log是逻辑日志，记录的是与当前操作相反的操作，如执行insert，就记录一条delete

## 二进制日志 binlog

记录所有修改数据库的操作，以及消耗的资源

主要在`备份`和`主从复制`场景中应用

二进制日志对所有操作进行记录，所以会影响性能，默认是`关闭的`

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

为了保证事务的持久性，应该将日志持久化到磁盘上，以innodb引擎为例，在事务commit之后：

- 1.写入binlog

- 2.写入redolog

- 3.决定这两个日志是否刷写到磁盘（调用fsync)

- 4.commit完成

主要通过两个参数`innodb_flush_log_at_trx_commit`（redolog）和`sync_binlog`（binlog）两个参数来配置刷写策略

对于redolog，innodb_flush_log_at_trx_commit的配置有三种：

- 1.值为`0`，log buffer`每秒一次`写入log file种，并且log file的`刷写操作（flush）同时进行`

- 2.值为`1`，每次`事务提交`时把log buffer写入log file，并`同时flush`

- 3.值为`2`，每次`事务提交`时把log buffer写入log file，但不同时flush，而是`每秒flush一次`

对于binlog，sync_binlog有两种策略：

- 1.值为`0`，依赖操作系统来刷写binlog，而不是mysql主动操作

- 2.值为`N(N>0)`，每`写N次`binlog，就调用一次`fdatasync()`进行刷写
