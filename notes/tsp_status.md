## TCP连接的状态

TCP连接有以下几种状态

- LISTEN：服务端等待连接

- SYN-SEND：发送方发送第一个SYN之后的状态

- SYN-RECV：接收方收到SYN和返回ACK并发送自己的SYN`之间`

- ESTABLISHED：正常传输数据

- FIN-WAIT-1：连接中断发送方发送完FIN

- CLOSE_WAIT：接收方收到FIN并回复完ACK，到发送自己的FIN`之间`

- FIN-WAIT-2：接收方接收到ACK，等待FIN

- LAST-ACK：接收方发送完FIN，等待ACK

- TIME_WAIT：发送方发送完最后的ACK之后

- CLOSE：连接关闭

在整个TCP通信过程中各个状态如下图所示，其中黄字表示在socket编程时对应的方法

[![gLcO78.png](https://z3.ax1x.com/2021/05/22/gLcO78.png)](https://imgtu.com/i/gLcO78)