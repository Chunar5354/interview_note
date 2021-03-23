协程切换最主要的是要`保存上下文`

在Python中可以通过生成器来实现，在Go中可以通过channel实现

下面通过简单的生产-消费者模型来查看在两种语言中协程的实现方式

## Python

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

## Go

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