HTTP版本差异

## HTTP1.0

HTTP1.0的特点是`无状态`与`无连接`

无状态就是服务端不会保存客户端的身份，这一点可以借助`cookie/session`机制来实现

无连接指的是每次发起HTTP请求，都要经历TCP3次握手、4次挥手，效率很低，并且导致`队头阻塞`（前一个请求响应之后下一个请求才能发送，如果前一个被阻塞，那后面的都会被阻塞）

## HTTP1.1

与HTTP1.0相比，HTTP1.1的改进如下：

- 长连接，新增了Connection字段，设置成keep-alive可以使连接不断开

- 管道化，可以不等第一个请求被响应就发送第二个请求，但响应的顺序按照`请求的顺序`返回，所以依然有阻塞问题

- 缓存处理，如果浏览器有资源的缓存，就不会发送请求

- 断点传输，可以将大资源分割

## HTTP/2

HTTP/2的特性有：

- 二进制分帧，不同于HTTP1.x基于`文本`的解析，HTTP2.0将数据分割成二进制`帧`，二进制的解析效率更高，帧包含以下几个部分：

Length，3字节，表示帧的长度

Type，1字节，表示当前帧的`类型`（可能是首部，数据实体或协商信息等等）

Flags，1字节，帧的标识

Stream Identifier，31位（前面有一个保留位共32位），`流的唯一ID`，表示当前帧属于哪个流

- 多路复用

每个HTTP/2连接可以包含多个并发打开的`stream流`（在客户端和服务器之间交换的独立的`双向帧序列`）

每个流中的消息由多个帧组成，这些帧可以`乱序发送`，最终根据流标识重新组装

这样就实现了使用`一个TCP连接`同时处理多个流，并且进行`交错的请求和响应`，避免了队头阻塞的问题

- 首部压缩

因为HTTP是无状态的，每个请求都需要首部来标识，产生很多重复的传输

HTTP/2维护一个首部信息表，只对`有改动的首部信息`进行更新，大大减少了冗余信息的传输

- 服务端推送

服务端可以`主动发送`页面相关信息（比如css和js），而不用等到浏览器在解析到相应位置时额外进行请求

## HTTP 3.0

HTTP3.0使用`QUIC`作为运输层协议，有以下几点优势：

- 快速建立连接

QUIC是基于`UDP`实现的，相比于TCP，它只需要`一次握手`就可以进行数据传输

- 多路复用，解决运输层对头阻塞

HTTP/2解决的队头阻塞只是在HTTP层，而TCP层仍然存在队头阻塞问题，因为TCP的`包之间互相有依赖`（要等前面ACK）

由于QUIC基于UDP，在同一条QUIC连接上建立多个stream流，但包之间互相`没有依赖`，前面的包丢失了不会影响后面包的传输

- 报文加密

TCP报文的首部没有加密，而QUIC全部加密

- 向前纠错

QUIC中每个数据包除了包含自身的内容，还包含一部分其它包的内容，所以少量的丢包可以通过其他包的`冗余数据`直接得到，而`无需重传`

- 连接迁移

TCP是基于IP与端口的4元组标识的，而IP地址会发生改变，改变时要重新建立连接

而QUIC的连接由一个`Connectino ID`标识，在整个传输过程中`不会改变`，即使切换网络，仍然可以继续传输