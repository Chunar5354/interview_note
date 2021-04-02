[参考](https://www.zhihu.com/question/36514327)

CDN(Content Delivery Network 内容分发网络)是建立并覆盖在承载网之上，由分布在`不同区域`的`边缘节点服务器群`组成的分布式网络

用户向某个站点发起请求时，该站点会通过CDN返回一个`离用户最近CDN节点`（返回边缘服务器的IP地址），来加速用户的访问，如果该节点有资源的缓存，就直接返回给用户，如果没有，CDN节点会向源站请求资源，缓存并返回给用户

[![ce6KAO.md.jpg](https://z3.ax1x.com/2021/04/02/ce6KAO.md.jpg)](https://imgtu.com/i/ce6KAO)