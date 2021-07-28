[参考](https://www.jianshu.com/p/54cc04190252)

浏览器缓存主要分为强缓存与协商缓存

## 强缓存

强缓存指的是不向服务器发起请求，直接从缓存中读取资源

强缓存会得到200响应状态码，并且在chrome中查看Network的Size一栏会看到`disk cache`或`memory cache`

强缓存可以通过设置两种HTTP header来实现：`Expries`或`Cache-Control`

- Expries

用来指定资源到期的时间，这个时间指的是服务器端的时间点

Expires=max-age+请求的时间点（Expires定义的是一个`绝对的时间点`），需要与Last-modified组合使用

Expires受限于`本地时间`，主要用于HTTP/1.0版本

- Cache-Control

Cache-Control是HTTP/1.1引入的，它可以在请求头或响应头中指定

如`Cache-Control:max-age=300`表示在请求返回的300秒内再次请求这个资源，就会命中强缓存

如果同时设置Expires和Cache-Control，则Cache-Control的优先级更高

Cache-Control常用的几个配置：

- 1.no-cache，表示不使用强缓存，浏览器每次必须向服务器验证缓存的有效性

- 2.max-age，表示自响应时间开始的缓存有效期，单位为秒

### 启发式缓存

如果响应头中没有设置Expires和Cache-Control，则会根据响应头中的`Date`字段值减`Last-Modified`字段值的`10%`作为缓存失效时间，这种方式称为启发式缓存

### disk cache 与 memory cache的区别

顾名思义，disk cache就是将资源缓存在磁盘上，memory cache就是将资源缓存在内存中

如果缓存在内存中，随着进程的关闭（浏览器页面关闭），缓存的内容就消失了

如果缓存在磁盘中，则可以存储更久，而且即使是跨站点，只要某个资源的地址相同，也能够命中缓存

通常大文件会被缓存在磁盘上，而且在系统内存使用率较高时会更倾向于使用磁盘缓存

## 协商缓存

协商缓存发生在`强缓存失效后`，浏览器携带缓存标识向服务器发起请求，服务器再根据缓存标识决定是否使用缓存

主要有两种情况：

- 1.协商缓存生效，返回`304 Not Modified`

- 2.协商缓存失效，返回`200 OK`与新的请求结果

协商缓存通过设置两个Header来实现：`Last-Modified`与`ETag`

### Last-Modified

在浏览器第一次访问资源时，服务器返回的header中包含Last-Modified，表示资源在服务器上的最后修改时间，浏览器接收到请求后缓存`资源文件`与`header`

在后面的请求中，浏览器发现缓存中有Last-Modified这个header，就会在请求头中添加`If-Modified-Since`字段，它的值就是Last-Modified的值，表示询问服务器在这个时间之后资源有没有更新

服务器接收到请求，将If-Modified_Since的值与资源的最后修改时间对比，如果没有变化，就返回`304 Not-Modified`，否则返回`200 OK`与新的资源

Last-Modified的缺点：

- 1.精度为`秒级`，如果在1秒内做了修改则识别不出来

- 2.`本地`打开缓存文件也会造成Last-Modified被修改，导致错误的缓存不命中

### ETag

ETag是服务器响应请求时，服务器为资源生成一个`唯一标识`并返回，只要资源发生了变化，ETag就会更新

浏览器在后续的请求中将最开始的ETag值放到`If-None-Match`字段中，服务器与本地的ETag比较，就可以判断资源是否被修改