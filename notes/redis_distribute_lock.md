## SETNX命令

Redis中的分布式锁由`SETNX`实现

当使用SETNX插入一个key时，如果这人key不存在，就正常插入，返回`1`，如果key已存在，就`什么也不做`，并返回`0`

用go+redis实现一个简单的分布式锁;

```go
var ctx = context.Background()
var num int64

func getnx(rdb *redis.Client) {
	val, err := rdb.Do(ctx, "setnx", "key", "value").Result()  // 获取锁
	t := time.Now()
	for val == num {
		val, err = rdb.Do(ctx, "setnx", "key", "value").Result()
		if err == redis.Nil {
			fmt.Println("key does not exists")
			return
		}
		// fmt.Println("blocked")
	}
	fmt.Println("waited:", time.Since(t))
	time.Sleep(time.Second*1)  // 在这里进行业务处理
	rdb.Do(ctx, "del", "key")  // 释放锁
}

func main() {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "123456",
		DB:       0,
	})
	for i := 0; i < 5; i++ {
		go getnx(rdb)
	}
	time.Sleep(time.Second*10)
}
```

将setnx作为分布式锁使用，在一开始调用setnx，如果结果返回1，说明当前goroutine`获取到了锁`，然后进行业务处理，最后要删除key`释放锁`

为防止某个进程出现错误，导致锁无法被正确释放，通常会通过`expire`命令设置一个`过期时间`

## 针对多节点的Redlock算法

[参考](https://juejin.cn/post/6844904039218429960)

如果存在多个节点，那么客户端每次访问哪个节点是不能够确定的，所以要保证每次上锁都`锁住了全部的节点`

Redlock算法提供了这样的实现，分为以下几个步骤：

- 1.客户端首先获取`本地时间`

- 2.从`全部的master节点`获取锁，为了避免某个master宕机导致通信时间太长，应该设置一个比锁的有效时间小得多的`超时时间`

- 3.客户端计算在获取锁过程中`消耗的时间`，当且仅当从`过半数`的节点中都获取到了锁，而且消耗的时间`小于`锁的有效时间，才认为该客户端获取到了锁

- 4.如果获取成功，真正执行任务的时间等于锁的有效时间`减去`消耗的时间

- 5.如果获取锁失败，则在`所有`的节点上释放锁

由于在过半数节点上获取到锁才认为获取成功，所以同一时刻只能有一个客户端获取锁

Redlock算法的不足：

- 1.如果客户端1获取到锁之后发生了阻塞，阻塞时长超过锁的过期时间，就有可能出现错误

- 2.Redlock算法依赖于`系统时间的一致性`，如果某个节点的时钟出现跳跃，那可能在判断`是否获取锁`以及`锁超时`的时候会出现错误
