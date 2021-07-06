## 进程线程协程对比

### 进程

进程是资源分配的最小单位，需要在内核态完成切换

进程的上下文包括：通用目的寄存器，程序计数器，用户栈，内核栈，虚拟地址空间（页表）等

进程的切换涉及到虚拟地址的转换，原来的页表缓存将不可用，所以开销很大

#### 进程的各种ID

- PID，进程号

- PPID，父进程的进程号

- PGID，进程组号

- SID，session号

session与group都是管理多个进程的方式，同一个group的进程属于一个session，一个session可以包含多个group

session与`终端`相关，同一个终端启动的进程默认在一个session中

子进程会`继承`父进程的PGID和SID

可以使用`ps ajx`来查看这些ID，而且其中的`tty`字段表示的是终端

tty字段中`pts/0`字样的表示虚拟终端，`?`表示没有终端（后台进程）

### 线程

线程依赖于进程，一个进程可以创建多个线程，它们共享这个进程的某些数据，线程之间有竞争，需要加锁

线程也由CPU在内核态调度

线程的上下文包括线程ID（TID），栈，栈指针，程序计数器，通用目的寄存器等

线程的ID由`线程组`维护，主线程的ID与它的`进程ID相同`，额外的每个线程都有`自己的进程ID`，但相同线程组的线程有相同的`TGID`

### 协程

协程在用户态，与线程是多对多的关系，它的上下文更小，而且`不需要加锁`，协程切换最主要的是要`保存上下文`

协程相比于线程的优势：

- 1.协程上下文切换发生在用户态，数据更轻量

- 2.线程的上下文切换可能随时发生，而协程是用户自定义的`显示切换`，上下文的保存更加轻量

传统协程的缺点（go通过GMP模型进行了改进）：

- 1.无法利用多核，传统的协程是运行在单线程上的，利用多核需要配合多进程

- 2.协程的阻塞会阻塞整个程序

## 协程实现生产-消费者模型

在Python中可以通过生成器来实现，在Go中可以通过channel实现

下面通过简单的生产-消费者模型来查看在两种语言中协程的实现方式

### Python

```python
def consumer():
    send_to_p = ''
    while True:
        # 将send_to_p传到外部，并接受外部传来的get_from_p参数
        get_from_p = yield send_to_p
        print('consumer:', get_from_p)
        send_to_p = 'after: {}'.format(get_from_p)

def producer(c):
    # 发送一个None值启动生成器
    c.send(None)
    for i in range(5):
        print('producer:', i)
        # 把i传进生成器，并从生成器中获取参数
        get_from_c = c.send(i)
        print(get_from_c)
    c.close()

c = consumer()
producer(c)
```

在上面代码中，consumer()是一个生成器，它通过yield语句可以实现`接收外部send()`传进来的参数，并且可以将生成器内部的值`传到外部（类似return）`

流程如下：

[![6HZAAO.png](https://z3.ax1x.com/2021/03/23/6HZAAO.png)](https://imgtu.com/i/6HZAAO)

### Go

```go
var N = 10

func consumer(m <-chan int) {
	for i := 0; i < N; i++ {
		message := <-m   // 消费者从channel中取出消息
		fmt.Println("consumer:", message)
	}
}

func producer(m chan<- int) {
	for i := 0; i < N; i++ {
		fmt.Println("producer:", i)
		m <- i  // 生产者向channel中添加消息
	}
}

func main() {
	m := make(chan int, 2)
	go producer(m)
	go consumer(m)
	time.Sleep(time.Second*2)
}
```

利用了读取空channel和写入满channel会`阻塞`的特性，用go原生的goroutine来实现

可以指定channel大小，更加灵活
