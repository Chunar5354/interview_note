IO多路复用是`单线程`监听多个文件描述符是否可以执行IO操作，本质上是`同步IO`

在Linux下有三种IO多路复用方式：select，poll和epoll

[参考1](https://rebootcat.com/2020/09/26/epoll_cookbook/)

[参考2](https://juejin.cn/post/6844904200141438984)

## select

select函数的定义如下：

```c
int select(
    int max_fd, 
    fd_set *readset, 
    fd_set *writeset, 
    fd_set *exceptset, 
    struct timeval *timeout
)
```

调用select函数时会在调用出`阻塞住`，直到有文件描述符可以`进行IO操作`、被信号`中断`或`超时`才会返回

select将监听的文件描述符分为三种：读（readset），写（write）以及异常（exceptset），传入的fd_set是一个`数组（bitmap）`，总长度默认是`1024位`

每次调用select会将传入的文件描述符从`用户态拷贝到内核态`，并开启`轮询`来遍历所有的文件描述符

### select的缺点：

- 1.单个进程打开的fd数量有限制，默认是1024

- 2.使用轮询的方法来遍历fd，时间复杂度为O(n)

- 3.每次调用select都需要要进行用户态到内核态的拷贝，当fd很多时，开销较大

## poll

与select使用三种不同的fd_set相比，poll使用一个pollfd结构体来表示要监听的文件描述符，通过链表进行组合，不再有`数量的限制`

```c
struct pollfd {
    int fd;                         // 需要监视的文件描述符
    short events;                   // 需要内核监视的事件
    short revents;                  // 实际发生的事件
};

// API
int poll(struct pollfd fds[], nfds_t nfds, int timeout);
```

其它方面与select基本相同

### poll的改进

poll解决了selectfd数量限制的问题，但仍然会有拷贝和O(n)的时间复杂度

## epoll

epoll的数据结构是eventpoll，使用红黑树来存储，调用epoll_wait时查询可用的fd并`阻塞`

```c
#include <sys/epoll.h>

// 数据结构
// 每一个epoll对象都有一个独立的eventpoll结构体
// 用于存放通过epoll_ctl方法向epoll对象中添加进来的事件
// epoll_wait检查是否有事件发生时，只需要检查eventpoll对象中的rdlist双链表中是否有epitem元素即可
struct eventpoll {
    /*红黑树的根节点，这颗树中存储着所有添加到epoll中的需要监控的事件*/
    struct rb_root  rbr;
    /*双链表中则存放着将要通过epoll_wait返回给用户的满足条件的事件*/
    struct list_head rdlist;
};

// API
int epoll_create(int size); // 内核中间加一个 ep 对象，把所有需要监听的 socket 都放到 ep 对象中
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event); // epoll_ctl 负责把 socket 增加、删除到内核红黑树
int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout);// epoll_wait 负责检测可读队列，没有可读 socket 则阻塞进程
```

### epoll解决的问题

- 1.没有fd数量的限制，而且相比poll的链表，epoll使用红黑树，访问更加高效

- 2.对于select和poll，每次调用都需要把所有的fd从用户态拷贝到内核态，而epoll在`内核空间`创建了一棵红黑树（事件表），应用程序把要监听的fd添加到红黑树中，这样就只需要在第一次监听这个fd的时候`拷贝一次`（首次调用epoll_ftl)，而不需要每次都拷贝

- 3.在eventpoll结构体中，有一个rd_list`保存就绪的fd`，这样就不需要遍历所有的fd，时间复杂度为O(1)，注意对rd_list的遍历是在`用户空间`完成的，需要从内核态拷贝到用户态，但是数量较少

### epoll的触发方式

epoll对于fd的访问有两种触发方式：水平触发（Level Trigger LT）和边沿触发（Edge Trigger ET），默认是LT

- LT：只要某个fd`可以读`，每次调用epoll_wait都会返回并通知应用程序进行IO操作

- ET：只有fd的`状态发生变化`，epoll_wait才会返回，比如上一次没有读完，且期间fd`没有被写入`（状态没变），下一次调用epoll_wait就不会返回，所以在使用ET模式的时候需要保证每次都`读完`fd的全部内容

### epoll的典型应用

- redis，默认使用LT

- nginx，默认使用ET