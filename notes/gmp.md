[参考](https://learnku.com/articles/41728)

## 为什么需要调度器

为了提高并发能力，同时运行多个进程（线程，协程）

进程具有大量的上下文资源，切换时开销很大

线程开销相对较小，但是多线程共用一个进程的虚拟地址空间，会发生竞争、锁等问题

把线程分为用户态和内核态，内核态的线程仍然由CPU调度，用户态的线程(协程)由`用户程序自行调度`，这样就减轻了CPU的负担

用户态的协程与内核态的线程时`M:N`的关系

## GMP模型

### G

G(goroutine)协程，每个G是结构体，G只有被添加到P之后才能被调度运行

goroutine的结构是[runtime.g](https://github.com/golang/go/blob/41d8e61a6b9d8f9db912626eb2bbc535e929fefc/src/runtime/runtime2.go#L404)

g中有大量的字段，其中比较重要的有几个：

```go
type g struct {
    stack        stack   // 当前goroutine的栈内存范围
    _panic       *_panic // 最内侧的panic结构体，是一个链表的节点
	_defer       *_defer // 最内侧的defer结构体，是一个链表的节点
	m            *m      // 当前占用的线程
	sched        gobuf   // 调度相关的数据
    atomicstatus uint32  // 状态
    preempt      bool    // 抢占信号
}
```

其中sched的gobuf类型存储了一些上下文信息，如程序寄存器、栈寄存器的指针等

atomicstatus是goroutine的状态，共有9种：

- 1.`_Gidle`，刚被分配，未被初始化

- 2.`_Grunnable`，存储在运行队列中，等待被执行

- 3.`_Grunning`，可以执行代码，被赋予了M和P

- 4.`_Gsyscall`，正在执行系统调用，拥有M但不在P上

- 5.`_Gwaiting`，运行时被阻塞，没有执行用户代码，不在P上，可能在channel的等待队列上

- 6.`Gdead`，没有被使用

- 7.`_Gcopystack`，栈正在被拷贝，没有使用，不在P上

- 8.`_Gpreempted`，因为被抢占而阻塞，没有执行用户代码，不在P上，等待唤醒

- 9.`Gscan`，GC在扫描栈空间，没有执行代码

### M

M(Mcahine)内核线程，M`不保存G的上下文`，所以G可以跨M

M的结构体是[runtime.m](https://github.com/golang/go/blob/41d8e61a6b9d8f9db912626eb2bbc535e929fefc/src/runtime/runtime2.go#L486)

几个比较重要的字段：

```go
type m struct {
    g0      *g        // m第一个创建的rogoutine，仅用于调取其它G
    curg    *g        // 当前运行的G
	p        puintptr // 当前运行的P
	nextp    puintptr // 暂存的P
	oldp     puintptr // 执行系统调用之前的P
}
```

### P

P(Processor)处理器

P能提供线程需要的`上下文`环境，也负责`调度`线程上的等待队列

P的结构是[runtime.p](https://github.com/golang/go/blob/41d8e61a6b9d8f9db912626eb2bbc535e929fefc/src/runtime/runtime2.go#L576)，重要的字段有：

```go
type p struct {
    m         muintptr       // 绑定的m
    status    uint32         // 状态
    runqhead  uint32    
	runqtail  uint32
	runq      [256]guintptr  // P的本地G队列，最多256个
    runnext   guintptr       // 下一个可运行的G
}
```

根据runqhead和runqtail`是否相等`和runnext来判断队列上有没有待运行的G

P的状态有5种：

- 1.`_Pidle`，没有运行用户代码或调度器，运行队列为空

- 2.`_Prunning`，被M持有，并正在运行用户代码或调度器

- 3.`_Psyscall`，当前线程陷入系统调用，没有执行用户代码

- 4.`_Pgcstop`，被M持有，由于垃圾回收被停止

- 5.`_Pdead`，当前P不被使用

### GMP的过程

m0和g0：

- 启动程序后首先创建一个初始线程`m0`，它负责初始化操作和启动第一个G，然后就变成普通的m

- 每个m都有一个`g0`，负责调度

流程：

- 在程序开始时会先创建m0和g0，并将二者绑定

- 初始化调度器、栈、GC，并根据GOMAXPROCS创建P，并将应用程序的`main groutine`添加到P的本地队列

- 启动m0，从P的本地队列获取G

- m根据G的栈和调度信息设置运行环境

- m运行G

- G运行完退出，m继续获取可运行的G，直到main.main退出

**类似于将P作为缓存来将G放到M上运行**

G有全局队列，每个P还有一个本地队列用来存放G，当新出现G的时候，优先放到P的`本地队列`中，P的数量可以通过`GOMAXPROCS`来设置，默认是`CPU核心数`

P和M的数量没有绝对的关系，当M阻塞时，P就会创建新的M（所以`M可能比P多`）

### GMP的优势

- 轻量调度

M在全局队列获取G的时候需要加锁，而在P的本地队列获取G则`不需要加锁`

- 复用线程

work stealing机制，当本线程没有可运行的G时，会尝试从其他线程绑定的P`偷取G`，而不是销毁当前线程

hand off机制，当本线程被阻塞时（因为G的系通过调用），释放绑定的P，交给其他空闲的线程
