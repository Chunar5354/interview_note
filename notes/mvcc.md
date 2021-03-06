MVCC，多版本并发控制，用来在多个事务并发执行时进行事务间的隔离

MVCC的优点在于能够实现一定程度的读写并发，且`不需要加锁`，缺点是增加了额外的`存储空间`和`判断`

MySQL中MVCC的实现是通过保存数据在某个时间点的`快照`来实现的（快照保存在undo log中），根据事务开始时间的不同，每个事务对同一张表同一时刻看到的内容可能是`不同的`

InnoDB的MVCC是通过在记录后面保存`两个隐藏列`来实现的，分别保存了当前行的`创建版本号`和`删除版本号`

MVCC只与读已提交和可重复读两个隔离级别兼容，对于MySQL，MVCC对各个操作的执行如下：

- SELECT：只查找版本`早于当前事务版本`的行，并且行的删除版本要么未定义，要么`大于当前事务版本号`，这样就保证该事务读到的数据在事务开始之前未被删除

- INSERT：为新插入的行保存`当前系统版本号`作为行创建版本号

- DELETE：为删除的行保存当前系统版本号作为行删除版本号

- UPDATE：为被更新的行保存当前系统版本号作为行创建版本号，同时为原来未更新时的行保存当前系统版本号作为行删除版本号（相当于将更新操作分成两部分，旧行删除并插入新行）

## 示例

innodb中每个事务都有一个`transaction id`，它是升序且唯一的

每当事务`更新数据`的时候，都会生成一个数据版本，并把事务的transaction赋值给这个数据版本的事务id，称为`row trx_id`

因此表中的同一行记录，可能拥有多个版本，这个版本保存在`undo log`中，新的版本有`指向旧版本`的指针

在事务启动时，innodb会为这个事务生成一个数组，用于保存当前`正在活跃`（开始但未提交）的所有事务id

所以全部的事务可以分成下图所示

[![WeAIM9.png](https://z3.ax1x.com/2021/07/14/WeAIM9.png)](https://imgtu.com/i/WeAIM9)

对于一个数据版本row trx_id：

- 如果落在最左侧，说明是已提交的事务或当前事务自己生成的，可见

- 如果落在最右侧，说明是由还未开始的事务生成的，不可见

- 如果落在中间，则分两种情况：
    - 如果row trx_id在当前事务的数组中，说明是由未提交的事务生成的，不可见
    - 如果不在数组中，说明是由已提交的事务生成的，可见


### 数据更新与当前读

对于不加lock的select语句，使用的是`快照读`，规则如上面描述的

对于加lock的select与update等数据更新操作，使用的是`当前读`

在当前读场景中，事务都会`尝试`读取`最新`row trx_id版本的数据（更新操作是`先读再写`），而不管数据的版本比自己新或旧，如果新版本的事务未提交，就要`等待`直到提交（锁释放）

### 例子

假设有以下三个事务：

[![Weni8K.md.png](https://z3.ax1x.com/2021/07/14/Weni8K.md.png)](https://imgtu.com/i/Weni8K)

- 对于事务A，由于A开始时，事务B与事务C均为开始，所以事务A执行`快照读`（select）的时候，不能看到B和C做的修改，最终查询的结果n仍然是`1`

- 对于事务B，B开始时，C未开始，但B的update语句执行的是`当前读`，并且在事务C提交后执行，所以事务B的update语句将n由2（事务C的更新）更新为了3，并且update之后，id=1这一行的数据版本变成了事务B的id：11，所以事务B的select能够看到自己所做的修改，得到结果为`3`

假设B执行update的时候C未提交，B就要`阻塞等待`
