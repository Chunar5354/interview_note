## Redis数据类型

Redis有5中基础数据类型

### STRING

STRING可以存储字符串、整数或浮点数

使用`SET`来创建与修改，`GET`获取键对应的值，`DEL`删除

```
> set server:name fido
OK
> get server:name
"fido"
> exists server:name
(integer) 1
> del server:name
(integer) 1
> exists server:name
(integer) 0
```

对于整数，可以使用`INCR`，`DECR`等操作来进行增减

```
> set num 9
OK
> incr num
(integer) 10
> decr num
(integer) 9
> incrby num 5
(integer) 14
```

对于浮点数，则可以使用`INCRBYFLOAT`来进行增减

```
> set num 1.1
OK
> incrbyfloat num 2.2
3.3
> incrbyfloat num -1.2
2.1
```

### LIST

LIST是一个双向的列表，可以从两边向其中添加和删除元素，以及范围操作

`RPUSH`从右端添加，`LPUSH`从左端添加

```
> rpush friends "Alice"
(integer) 1
> rpush friends "Bob"
(integer) 2
> lpush friends "Sam"
(integer) 3
```

`LRANGE`从左到右范围查询，带两个参数指定范围（`闭区间`），也可以是负数，`-i`表示倒数第i个元素

```
> lrange friends 0 -1
1) "Sam"
2) "Alice"
3) "Bob"
> lrange friends 0 2
1) "Sam"
2) "Alice"
3) "Bob"
> lrange friends 0 1
1) "Sam"
2) "Alice"
> lrange friends 0 -2
1) "Sam"
2) "Alice"
```

`LPOP`从左端弹出，`RPOP`从右端弹出

```
> lpop friends
"Sam"
> rpop friends
"Bob"
> llen friends
(integer) 1
```

### SET

SET是无序集合，可以添加、获取单个元素，计算交集、并集等

`SADD`添加元素，`SREM`删除元素

```
> sadd superpowers "flight"
(integer) 1
> sadd superpowers "flight"  // 添加已存在的元素会返回0
(integer) 0
> sadd superpowers "x-ray vision" "reflexes"  // 可以同时添加多个元素
(integer) 2
> srem superposers "reflexes"  // 如果集合中有这个元素，就返回1
1
> SREM superpowers "making pizza"  // 没有则返回0
0
```

`SMEMBERS`列出集合中所有元素，`SISMENBER`查询某个元素是否在集合中

```
> smembers superpowers
1) "x-ray vision"
2) "flight"
> sismember superpowers "flight"
(integer) 1
> sismember superpowers "making pizza"
(integer) 0
```

`SUNION`计算两个集合的并集，`SINTER`计算交集，`SDIFF`计算差集

```
> SADD birdpowers "pecking"
(integer) 1
> SADD birdpowers "flight"
(integer) 1
> SUNION superpowers birdpowers
1) "x-ray vision"
2) "pecking"
3) "flight"
> sinter superpowers birdpowers
1) "flight"
> sdiff superpowers birdpowers
1) "x-ray vision"
```

`SPOP`随机取出集合中的n个元素

```
> SADD letters a b c d e f
(integer) 6
> spop letters 3
1) "a"
2) "c"
3) "e"
```

### ZSET

ZSET是有序集合，在ZSET中每个元素都有一个`score`字段用来排序

`ZADD`添加元素，三个参数：集合名，score和value

```
ZADD hackers 1940 "Alan Kay"
ZADD hackers 1906 "Grace Hopper"
ZADD hackers 1953 "Richard Stallman"
ZADD hackers 1965 "Yukihiro Matsumoto"
ZADD hackers 1916 "Claude Shannon"
ZADD hackers 1969 "Linus Torvalds"
ZADD hackers 1957 "Sophie Wilson"
ZADD hackers 1912 "Alan Turing"
```

`ZRANGE`按照顺序取出范围内的元素

```
> ZRANGE hackers 2 4
1) "Claude Shannon"
2) "Alan Kay"
3) "Richard Stallman"
```

`ZREM`删除元素

```
> zrem hackers "Alan Kay"
1
```

### HASH

HASH的元素是键值对

`HSET`创建键值对或修改值，`HGET`根据键查找值，`HGETALL`找出全部键值对

```
> HSET user:1000 name "John Smith"
1
> HSET user:1000 email "john.smith@example.com"
1
> HSET user:1000 password "s3cret"
1
> HGETALL user:1000
1) "name"
2) "John Smith"
3) "email"
4) "john.smith@example.com"
5) "password"
6) "s3cret"
> HGET user:1000 name
"John Smith"
```

`HDEL` 删除某个键

```
> hdel user:1000 name
(integer) 1
> hgetall user:1000
1) "email"
2) "john.smith@example.com"
3) "password"
4) "s3cret"
```

## 底层数据结构

再redis-cli中，可以通过下面的命令来查看某个key的底层数据类型

```
object encoding key
```

### STRING

整性int，简单动态字符串（embstr，raw）

小于`39字节`的字符串用embstr编码，大于39字节用raw编码

embstr申请的内存是`连续`的，raw不一定

### LIST

快速列表quicklist，由压缩列表和双向链表组成

元素较少的时候压缩列表是`顺序IO`

### SET

整数集合intset，哈希表hashtable

### ZSET

压缩列表ziplist，跳表skiplist

### HASH

哈希表，压缩列表

## 跳表

跳表是在普通的链表基础上加了`索引层`，从而优化了查找操作，达到类似二分查找的`O(log(n))`时间复杂度

[![c3h5Mn.png](https://z3.ax1x.com/2021/04/07/c3h5Mn.png)](https://imgtu.com/i/c3h5Mn)

Redis中跳表是一个`双向链表`，且新建节点的时候`层数是随机的`