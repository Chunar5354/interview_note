Redis是内存数据库，为了防止断电丢失的问题，需要对数据做持久化处理

Redis有两种数据持久化方式：RDB和AOF

## RDB

RDB（Redis Database）是将Redis内存中的数据写到`RDB文件`中保存到磁盘上来实现持久化

在Redis客户端中，通过`save`来保存(阻塞)，或`bgsave`创建`子进程`在后台保存(非阻塞，需要复制当前的数据快照)

也可以配置`redis.conf`自动保存，如：

```
save 900 1
```

表示在`900秒`内发生了`1次写操作`就触发`bgsave`命令

RDB文件是一个二进制文件，相当于数据快照，可以将它复制到其它主机上创建副本

优点：

- 1.文件紧凑，全量备份

- 2.bgsave时会fork一个子进程来负责保存，主进程不会进行IO操作

- 3.在恢复大数据集时RDB比AOF快

缺点：

- 1.子进程会复制父进程的全部数据，占用空间

- 2.复制过程中父进程的修改不会体现在子进程中，可能`丢失数据`

## AOF

AOF（Append Only File）是将`写操作`添加到AOF文件的末尾，也是通过fork子进程来实现的

通过修改`redis.conf`来配置

```
appendonly yes                       # 开启AOF持久化
appendonlyfilename "appendonly.aof"  # AOF文件路径
appendfsync always/everysec/no       # 写入与同步策略
```

写入与同步策略有三种，always是`每写一次命令`都同步，everysec是`每秒`同步一次，no是操作系统自动同步

默认是everysec

AOF文件中存的是`写入的命令`，如执行一条：

```
set name 111
```

AOF文件的内容将是：

```
*2
$6
SELECT
$1
0
*3
$3
set
$4
name
$3
111
```

如果多次修改name的值，就会记录多条语句，但其实只有最后的修改是有用的，此时就产生了`数据冗余`

可以通过命令

```
BGREWRITEAOF
```

来消除冗余，或者配置`redis.conf`文件：

```
auto-aof-rewrite-percentage 100    // AOF超过指定比例时重写
auto-aof-rewrite-min-size 64mb     // AOF超过指定大小时重写
```

在进行数据恢复时，将AOF文件中的指令一条一条读取并执行

如果同时设置了RDB和AOF会根据`AOF`来恢复，因为AOF写入的频率更高

优点：

- 1.AOF能更好的保护数据不丢失（因为写入频率高）

- 2.AOF文件的可读性更好，在恢复时比较灵活

- 3.AOF是`追加`的写方式，顺序IO写入性能更高

- 缺点：

- 1.相比RDB，AOF文件更大

- 2.AOF中记录的是数据发生变化的命令，在恢复时比较依赖现有的数据，可能会出错
