MySQL主要的存储引擎有两个：InnoDB和MyISAM

## InnoDB

InnoDB是MySQL当前的默认存储引擎，它是`事务型`的，默认的隔离级别是`可重复读`，并通过MVCC和间隙锁来防止幻读

InnoDB的表结构文件为`.frm`，数据与索引存放在`.idb`文件中

InnoDB的索引是`聚簇索引`，它将数据放在B+树的叶子节点中，对于主键查询有很高的性能

只有InnoDB支持`热备份`

## MyISAM

MyISAM`不支持事务`

MyISAM不支持行级锁，只能对`整张表`加锁，可以在`读取的同时写入`（并发插入）

MyISAM表可以手动或自动修复，但修复时可能导致数据丢失，而且修复操作很慢

MyISAM设计简单，数据存储紧密，提供了压缩表和空间数据索引等特性

## 区别

- 1.InnoDB支持事务，而MyISAM不支持

- 2.InnoBD支持外键，而MyISAM不支持

- 3.InnoDB支持行级锁，MyISAM不支持

- 4.InnoDB支持热备份，MyISAM不支持

- 5.InnoDB的索引是聚簇索引，数据直接存在索引的叶子节点上，而MyISAM是非聚簇索引，索引中保存的是指向数据的指针

- 6.InnoDB不保存总行数，而MyISAM保存

- 7.MyISAM的数据安全性要比InnoDB差，崩溃后容易损坏