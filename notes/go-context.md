[参考](https://draveness.me/golang/docs/part3-runtime/ch06-concurrency/golang-context/)

Go的上下文包context主要用来进行goroutine中`设置截止时间`、`同步信号`与`传递请求`相关的操作

## Context接口

主要的接口是context.Context:

```go
type Context interface {
	Deadline() (deadline time.Time, ok bool)
	Done() <-chan struct{}
	Err() error
	Value(key interface{}) interface{}
}
```

它包含四个方法：

- 1.Deadline，返回context.Context被取消的时间

- 2.Done，返回一个channel，在当前工作完成或上下文被取消后会`关闭`

多个goroutine同时订阅channel中的消息，来实现同步（看参考中的例子）

- 3.Err，返回context.Context结束的原因，只有在Done返回的channel被关闭时返回`非空`的值

- 4.Value，获取键对应的值，可以用来传递请求的数据

## 默认上下文

很多的扩展库如redis等都要传入上下文作为参数，常用的有background和todo

它们都是实现了Context接口的空类型`context.emptyCtx`，没有任何功能，实际的上下文会通过它来扩展

- context.Background是上下文的`默认值`，所有的其它上下文都从它衍生出来

- context.TODO主要在不确定使用哪种上下文时使用