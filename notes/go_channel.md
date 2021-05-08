[参考](https://draveness.me/golang/docs/part3-runtime/ch06-concurrency/golang-channel/#644-%E5%8F%91%E9%80%81%E6%95%B0%E6%8D%AE)

## 设计原理

channel是一个`先入先出`的数据管道，用于在不同的goroutine之间传递消息

有以下三种类型：

- 1.同步channel，没有缓冲区，发送方直接将数据传给接收方（handoff）

- 2.异步channel，基于环形缓存队列，生产者消费者模型

- 3.chan struct{}类型的异步channel，struct{}类型`不占用内存空间`，也不实现缓冲区和直接发送的语义

## 数据结构

channel的数据结构是在`runtime.hchan`中定义的

```go
type hchan struct {
	qcount   uint           // Channel中的元素个数
	dataqsiz uint           // Channel循环队列的长度
	buf      unsafe.Pointer // 缓冲区处理指针
	elemsize uint16         // Channel中操作的元素的大小
	closed   uint32         // 表示Channel是否被关闭的状态
	elemtype *_type         // Channel中操作的元素的类型
	sendx    uint           // 发送操作处理到的位置
	recvx    uint           // 接收操作处理到的位置
	recvq    waitq          // 由于缓冲区空间不足而阻塞的发送方goroutine队列
	sendq    waitq          // 由于缓冲区空间不足而阻塞的接收方goroutine队列

	// lock protects all fields in hchan, as well as several
	// fields in sudogs blocked on this channel.
	//
	// Do not change another G's status while holding this lock
	// (in particular, do not ready a G), as this can deadlock
	// with stack shrinking.
	lock mutex              // 在操作时会锁住整个Channel
}
```

其中recvq和sendq的数据结构是`runtime.waitq`，它包含一个双向链表的头和尾节点指针

```go
type waitq struct {
	first *sudog
	last  *sudog
}
```

`runtime.sudog`表示在阻塞队列中的goroutine，它是一个`双向链表`的节点

```go
type sudog struct {
	// The following fields are protected by the hchan.lock of the
	// channel this sudog is blocking on. shrinkstack depends on
	// this for sudogs involved in channel ops.

	g *g

	next *sudog
	prev *sudog
	elem unsafe.Pointer // data element (may point to stack)

	// The following fields are never accessed concurrently.
	// For channels, waitlink is only accessed by g.
	// For semaphores, all fields (including the ones above)
	// are only accessed when holding a semaRoot lock.

	acquiretime int64
	releasetime int64
	ticket      uint32

	// isSelect indicates g is participating in a select, so
	// g.selectDone must be CAS'd to win the wake-up race.
	isSelect bool

	parent   *sudog // semaRoot binary tree
	waitlink *sudog // g.waiting list or semaRoot
	waittail *sudog // semaRoot
	c        *hchan // channel
}
```

## 创建channel

通过`make`来创建channel，会根据传入的`数据类型`和`缓冲区大小`来创建channel结构

分为几种情况：

- 1.如果没有缓冲区，就只为channel分配内存空间

- 2.如果channel操作的数据`不是指针`类型，就为channel和底层的数组（缓冲区）分配一块`连续`的内存空间

- 3.如果是其他情况，`单独`为channel和缓冲区分配内存

## 发送数据

向channel中发送数据是通过`runtime.chansend`来实现的

```go
func chansend(c *hchan, ep unsafe.Pointer, block bool, callerpc uintptr) bool {
    ...
    // 加锁并判断当前channel是否关闭
	lock(&c.lock)

	if c.closed != 0 {
		unlock(&c.lock)
		panic(plainError("send on closed channel"))
	}
    ...
}
```

发送时有三种情况：

- 1.有`正在等待的接收者`，则通过`runtime.send`直接将数据发送给接收者，该函数的执行分为两部分：

    - 将发送的数据拷贝到`x = <- c`中x所在的内存地址上

    - 将等待接收数据的goroutine标记成`可运行状态`，并把该goroutine放到所在的处理器的`runnext`上等待执行，处理器在下一次调度时会`立即唤醒`这个goroutine

- 2.当缓冲区存在`剩余空间`时，将要发送的数据写入channel的缓冲区

- 3.当没有接收者也没有缓冲区剩余空间时，当前发送操作将被`阻塞`，主要有以下几个步骤：

    - 获取当前的goroutine，并根据它创建一个新的等待队列节点`sudog`

    - 将这个sudog加入`发送等待队列`，并设置到当前goroutine的waiting上，表示它正在等待sudog准备就绪

    - 将当前goroutine陷入沉睡`等待唤醒`，让出处理器的使用权


## 接收数据

接收数据有两种方式

```go
i <- ch
i, ok <- ch
```

它们最终都会调用`runtime.chanrecv`：

```go
func chanrecv(c *hchan, ep unsafe.Pointer, block bool) (selected, received bool) {
	if c == nil {
		if !block {
			return
		}
		gopark(nil, nil, waitReasonChanReceiveNilChan, traceEvGoStop, 2)
		throw("unreachable")
	}

    // 加锁并判断是否关闭
	lock(&c.lock)

	if c.closed != 0 && c.qcount == 0 {
		unlock(&c.lock)
		if ep != nil {
			typedmemclr(c.elemtype, ep)
		}
		return true, false
	}
}
```

接收数据也存在三种情况：

- 1.当存在`等待的发送者`时，通过`runtime.recv`从获取数据，这里也包含两种情况：

    - （1）如果channel`没有缓冲区`，就直接将channel发送队列中的goroutine的数据拷贝到接收方的目标地址

    - （2）如果channel`有缓冲区`，则将`缓冲区头部的数据`拷贝到目标地址，并将`发送队列头部的数据`拷贝到缓冲区，释放一个阻塞的发送方goroutine

- 2.当没有等待的发送者，且`缓冲区存在数据`时，从缓冲区的头部复制数据到目标地址

- 3.当没有等待的发送者，且`缓冲区不存在数据`时，当前的接收goroutine`休眠`并等待其它goroutine向channel发送数据