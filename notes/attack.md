## SYN洪泛攻击

向服务器发送大量的SYN请求，但`不进行第三次握手`，由于服务器在第二次握手的时候就已经分配了资源（半连接状态），等不到客户端的响应就会一直保持资源的分配，如果恶意请求量很大的话可能导致服务器崩溃

解决办法：服务器不在第二次握手的时候分配资源，而是为客户端分配一个`cookie`用于标识身份，当客户端第三次握手发送ACK的时候会带上这个cookie，服务器认出他是合法的客户端，此时再为连接分配资源buk

## RST攻击

当连接出现异常时，会发送RST报文，强制中断连接

比如像已经建立的连接发送SYN报文

## XSS攻击

跨站脚本攻击(Cross Site Scripting, CSS)，为了区别于层叠样式表(Cascsding Style Sheets)而写成`XSS`

XSS指的是攻击者A在向被攻击者B的网站进行`输入`时输入了一段`带有HTML标签的内容`，可能包含Javascript脚本，而B就会按照HTML的规则解析这段内容，从而被攻击

预防方式：对需要用户从输入的地方进行`转义和过滤`

[参考](https://tech.meituan.com/2018/09/27/fe-security.html)

## CSRF攻击

跨站请求伪造(Cross-site Request Forgery)

用户B在访问正常网站C之后访问了攻击者A的页面，由于此时B还保留着关于C的cookie，所以此时攻击者A可以`冒充B向C发起请求`（通常是为B的请求设置一个过滤规则进行转发），C会将A验证为B，这样A就可以用B的身份进行操作

预防方式：由于在CSRF攻击中，攻击者A`只是冒用`了B的信息，并不能真正获取到信息，所以C可以给每个用户一个`Token`对访问者进行验证

使用token可以防止csrf攻击，因为token并不会由浏览器自动添加到headers中

[参考](https://tech.meituan.com/2018/10/11/fe-security-csrf.html)


## DNS劫持

通过篡改DNS服务器中域名与IP的映射，将映射`指向错误的IP地址`

## DNS放大

利用伪造的IP地址（受害者的IP地址）向DNS服务器发起请求，导致受害者IP地址收到大量DNS服务器的响应

## DoS攻击

Dos是Denial of Service（拒绝服务攻击）的简称

指的是`攻击服务器`导致服务器不可用，比如使用SYN洪泛攻击

## DDoS攻击

DDos是Distributed Denial os Service（分布式拒绝服务攻击）的简称

指的是通过控制大量的感染恶意软件的计算机（称为僵尸网络）来对某个服务器发起攻击
