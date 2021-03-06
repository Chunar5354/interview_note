缓存的一些问题场景

## 缓存穿透

查询一条根本`不存在`的数据，数据库和缓存中都没有，所以每次都会访问到数据库

### 解决方法

- 1.第一次到数据库中查询发现不存在，在缓存中将key的`值设为空`，下一次就可以直接返回

- 2.布隆过滤器

## 缓存击穿

在高并发场景中，`大量的请求`查询同一个key，而这个key`刚好失效`，请求就会打到数据库

### 解决方法

在第一个线程用`互斥锁`对这个key加锁，在数据库中查询到后`存到缓存`里，这样后面的请求就可以在缓存中拿到数据

## 缓存雪崩

`大规模`的缓存同时失效，比如缓存服务器发生故障宕机

### 解决方法

- 1.设计方案时使用`缓存集群`

- 2.发生雪崩时使用熔断机制进行`限流`（限制某个服务只能同时被b个线程调用）和`降级`（只提供原来服务的缩小版，以减轻压力）

## 热点数据集中失效

设置缓存时，通常会设置过期时间，对于热点数据，失效后就会有大量的请求打到数据库

### 解决方法

- 1.设置随机过期时间

## 双写不一致

每次数据的更新需要更新数据库和缓存，但这两个操作之间可能会有延迟，会导致数据库和缓存中的内容不一致

[![cuIQEQ.png](https://z3.ax1x.com/2021/04/04/cuIQEQ.png)](https://imgtu.com/i/cuIQEQ)

如上图所示，在线程A更新数据库之后发生了延迟，此时线程B进行了更新，最终数据库里a=2，但缓存里a=1，出现了不一致的情况

### 解决方法

- 1.在`读多写少`的场景下，为操作加`读写锁`，就可以保证一致性

- 2.在对实时性要求较低的场景（如电商秒杀时看到的货物库存），可以对缓存进行`延时双写`，比如上面的线程B，在延时一定时间后再向缓存中写入一次，就能够实现一致性