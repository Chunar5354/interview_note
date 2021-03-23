Domain Name System（DNS，域名系统）提供主机名到IP地址的转换

- DNS是由`分层`的DNS服务器实现的`分布式数据库`

- 是`应用层`协议

- 运行在`UDP`上，端口是`53`

## 层次

DNS服务器以层次方式组织，分为三层：根DNS服务器、顶级域（Top-Level Domain TLD）DNS服务器以及权威DNS服务器

[![6TDRuq.png](https://z3.ax1x.com/2021/03/23/6TDRuq.png)](https://imgtu.com/i/6TDRuq)

- 根DNS服务器，它提供TLD服务器的IP地址

- TLD，TLD是根据顶级域组织的（如com, cn, org等），它提供权威DNS服务器的IP地址

- 权威DNS服务器，每个组织有自己的公共可访问的DNS记录（如 www.baidu.com)，存储在权威DNS服务器中，提供主机名到IP地址的映射

在这三个层次之外还有一个`本地DNS服务器`，用于代理本地主机发起DNS查询

DNS服务器通常是有`缓存`的，如果要查询的域名没有被缓存，就要向`上一级`DNS服务器查询

## DNS记录

每个DNS服务器都存储资源记录（Recourse Record RR），它是一个4元组，包含以下信息：

```
(Name, Value, Type, TTL)
```

TTL表示记录应该从缓存被删除的时间

Name和Value由Type决定，主要有以下几种：

- Type = A（Address），则Name是主机名，Value是主机的IP地址

- Type = NS（Name Server），则Name是域，Value是使用哪个权威DNS服务器来解析这个域

- Type = CNAME（Canonical Name），则Name是一个别名，Value是原本的规范主机名，CNAME用于将多个域名指向同一个主机

## 其它

- 为什么DNS使用UDP：DNS报文比较小，使用UDP不需要建立连接的过程，减轻服务器负载。而在有些时候报文长度很大时（比如区域传输），DNS`也可以使用TCP`

- DNS可以实现`负载均衡`，即一个域名对应多个IP