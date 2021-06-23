[参考1](https://rebootcat.com/2020/09/26/epoll_cookbook/)

[参考2](https://juejin.cn/post/6844904200141438984)

操作系统监听IO时，如果使用阻塞IO，在没有事件发生之前，进程会一直挂起，如果使用非阻塞IO，会立即返回，但需要不断轮询

使用IO多路复用技术可以利用`单个线程`同时监听多个IO连接（socket文件描述符），中间有一个文件描述符`就绪`就返回，否则`阻塞`直到超时，所以IO多路复用也叫`事件驱动`

有三种常用的IO多路复用方式：select，poll和epoll

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

调用过程为：

- 1.首先将fd_set从用户空间`拷贝`到内核空间

- 2.阻塞直到有`就绪的fd`或者`超时`

- 3.`遍历`fd_set，找到就绪的fd

- 4.将fd_set从内核空间`拷贝`到用户空间，由用户程序处理就绪的fd


### select的缺点：

- 1.select单进程支持监听的fd数量很小，32位机器是`1024`个，64位机器是`2048`个

- 2.每次调用需要将所有fd从用户态`拷贝`到内核态，开销很大

- 3.寻找就绪的fd时遍历的时间复杂度是`O(n)`，开销也很大

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

调用过程：

- 1.调用epoll_create创建eventpoll

- 2.调用epoll_ctl为fd注册要监听的事件，并为每个fd指定一个回调函数（用于添加就绪fd到list_head中），然后将整个eventpoll并`拷贝`到内核态

- 3.调用epoll_wait，阻塞等待就绪fd，一旦fd就绪，就出发它的回调函数，将这个fd添加到list_head中，所以只需要到list_head中处理相应的fd即可

优点：

- 1.epoll的监听fd数量上限时`最大可打开的文件数量`，远高于select的1024（1GB内存10万作用），而且相比poll的链表，epoll使用红黑树，访问更加高效

- 2.epoll在`内核空间`创建了一棵红黑树（事件表），应用程序把要监听的fd添加到红黑树中，这样就只需要在第一次监听这个fd的时候`拷贝一次`（首次调用epoll_ctl)，而不需要每次都拷贝

- 3.查找就绪fd时只需要到双向链表list_head中，时间复杂度是`O(1)`

### epoll的触发方式

epoll对于fd的访问有两种触发方式：水平触发（Level Trigger LT）和边沿触发（Edge Trigger ET），默认是LT

- LT：只要某个fd`可以读`，每次调用epoll_wait都会返回并通知应用程序进行IO操作

- ET：只有fd的`状态发生变化`，epoll_wait才会返回，比如上一次没有读完，且期间fd`没有被写入`（状态没变），下一次调用epoll_wait就不会返回，所以在使用ET模式的时候需要保证每次都`读完`fd的全部内容

ET的效率更高，适合大数据和非阻塞的socket，但要由用户自己判断读写是否完成的问题

### epoll的典型应用

- redis，默认使用LT

- nginx，默认使用ET