## HTTP状态码

### 1XX 信息性状态码

表示请求已接受，需要继续处理

### 2XX 成功状态码

返回以2开头的状态码表示请求已经正常处理完毕

- 200 OK，表示客户端的请求在服务端被正常处理

- 204 No Content，表示请求成功处理，但`不返回`响应报文的`主体`

- 206 Partial Content，表示响应了客户端的`范围请求`，返回了指定范围内的内容

### 3XX 重定向状态码

表示服务器为了处理请求进行了额外的操作

- 301 Moved Permanently，`永久性重定向`，表示所请求的资源已经更新了新的URI，而旧的URI已经删除了（如切换域名）

- 302 Found，`临时性重定向`，表示请求的资源更新了URI，但是旧的URI还能用（如未登录时访问，则切换到登陆页面）

- 303 See Other，所请求的资源有另一个URI，并让客户端使用`GET`方法访问新的URI

- 304 Not Modified，告诉客户端使用`缓存`即可

- 307 Temporary Redirect，与302意义相同，但是不从POST变成GET

### 4XX 客户端错误

表示客户端发送的请求有问题

- 400 Bad Request，表示报文中存在`语法错误`

- 401 Unauthorized，表示发送的请求需要有通过HTTP认证的认证信息

- 403 Forbidden，对请求资源的访问`被服务端拒绝`，可能是由于没有权限

- 404 Not Found，服务器上无法找到所请求的资源

### 5XX 服务端错误

表示服务端在处理请求时发生错误

- 500 Internal Server Error，服务器执行请求时发生了错误

- 501 Not Implemented，服务器不支持当前请求所需要的功能

- 503 Service Unavailable，服务器`暂时不可用`，可能是负载过大或正在维护