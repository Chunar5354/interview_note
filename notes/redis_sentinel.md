Redis哨兵用于在集群中`监测master节点`，在master节点挂掉时，从它的salve节点中选出一个新的master节点

工作方式如下：

- 1.每个sentinel节点每秒钟向其他所有节点发送`PING`

- 2.如果有一个节点的响应超时，就会被哨兵标记为`主观下线（SDOWN）`

- 3.如果master节点被标记为SDOWN，则正在监视这个master的所有哨兵都要以每秒一次的频率去确认这个master为主观下线

- 4.当有一定数量的哨兵都标记了一个master为SDOWN后（数量根据配置文件），则这个master被标记为`客观下线ODOWN`

- 5.一个被标记为SDOWN的master就被认为是挂掉了，会在它的slave节点中选出一个新的master