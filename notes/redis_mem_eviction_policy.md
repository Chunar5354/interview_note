Redis是内存数据库，为了更高效地利用内存，可以设置一个内存占用最大值，当超过最大值时，就删除掉一些已存在的内容

通过修改`redis.conf`文件来配置

```
maxmemory <bytes>       // 设置最大内存占用量
maxmemory-policy xxx    // 设置内存淘汰策略
```

目前的5.0版本中，Redis有8种内存淘汰策略：

- 1.volatile-lru，从设置过期时间的key中选择最近未使用的淘汰

- 2.allkeys-lru，从所有key中选择最近未使用的淘汰

- 3.volatile-lfu，从设置过期时间的key中选择最近最少使用的淘汰

- 4.allkeys-lfu，从所有key中选择最近最少使用的淘汰

- 5.volatile-random，从设置过期时间的key中随机选择一个淘汰

- 6.allkeys-random，从所有key中随机选择一个淘汰

- 7.volatile-ttl，从设置过期时间的key中选择`最快要过期`的淘汰

- 8.noeviction，`禁止`驱逐数据，在达到内存占用量时`报错`