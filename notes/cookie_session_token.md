cookie，session与token都是用于用户身份验证，本文主要介绍它们的特点和区别

## cookie

由于HTTP是无状态的协议，为了在多次请求之间保持用户登陆状态，在`客户端`（浏览器）保持一块数据。每次发送请求时携带它以表明身份

cookie是`不可跨域`的，浏览器会为每个域名保存不同的cookie，不同域名的cookie不能共享

### 使用cookie要注意的问题

- 1.每次请求都要携带cookie，所以体积不能太大

- 2.安全性

- 3.cookie`不能跨域`

- 4.浏览器缓存清理时cookie会被清除掉

- 5.移动端对cookie支持较差

## session

session保存在`服务器端`，通过将`sessionID`存入客户端的cookie，每次服务器接受请求时，从cookie中取出sessionID，再根据sessionID查找对应的session来进行验证

### session与cookie区别

- 1.cookie存储在客户端，session存储在服务器

- 2.cookie可以持续较长时间，session过期时间一般较短

- 3.session的体积可以比较大，且可以是任意数据类型，cookie只支持`字符串`

### 使用session注意的问题

- 1.在用户量较大时session比较占用服务器资源

- 2.集群式部署时在不同服务器上的session一致性问题

## token

在用户初次登陆成功后，服务器签发一个token交给客户端，服务器并`不保存token`，之后客户端每次请求时携带token，服务器收到token后进行验证（通过`计算`，而不是查找比对）

token完全由应用管理，所以可以`跨域`

token可以和session同时存在

### JWT

JWT（Json Web Token）是一种比较流行的`跨域认证`方案

JWT与普通token相似，但普通的token不包含用户信息，服务器在验证了token之后仍然需要到数据库中取查询用户信息，而JWT中`包含了用户信息和数据`，减少了对数据库的访问


