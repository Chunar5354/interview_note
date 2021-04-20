## Mutex

[参考1](https://draveness.me/golang/docs/part3-runtime/ch06-concurrency/golang-sync-primitives/#rwmutex)

[参考2](http://yangxikun.com/golang/2020/02/15/golang-sync-waitgroup.html)

### 数据结构

Mutex指的是互斥锁（mutual exclusion lock），在Go中的数据结构是`sync.Mutex`

```go
type Mutex struct {
	state int32    // 表示互斥锁的状态
	sema  uint32   // 用于控制锁状态的信号量
}
```

### 状态

互斥锁的state状态字段包含四个部分

[![cTX70U.png](https://z3.ax1x.com/2021/04/20/cTX70U.png)](https://imgtu.com/i/cTX70U)

- mutexStarving，`1位`，置位时表示互斥锁进入`饥饿状态`

- mutexWoken，`1位`，置位时表示表示互斥锁从`正常模式`被`唤醒`

- mutexLocked，`1位`，置位时表示互斥锁被`锁定`

- waitersCount，29位，表示当前互斥锁上等待的goroutine个数

初始时三个状态都是`0`

### 正常模式与饥饿模式

正常模式下，锁的等待者按照`先进先出`的顺序获取锁，但是刚被唤起的goroutine与新创建的goroutine进行竞争时，大概率会`获取不到锁`

为此，当有goroutine`超过1ms`没有获取到锁，它就将当前互斥锁切换为`饥饿模式`，防止有goroutine被饿死

在饥饿模式下，互斥锁会直接交给等待队列`最前面`的goroutine，新产生的goroutine会被`添加到队列末尾`等待

当有goroutine在`1ms内`获取到了锁，或者获取到锁的goroutine在`队列尾`，就将互斥锁切换到`正常模式`

### 加锁

通过`sync.Mutex.Lock`函数来进行加锁

```go
func (m *Mutex) Lock() {
	// Fast path: grab unlocked mutex.
	if atomic.CompareAndSwapInt32(&m.state, 0, mutexLocked) {
		if race.Enabled {
			race.Acquire(unsafe.Pointer(m))
		}
		return
	}
	// Slow path (outlined so that the fast path can be inlined)
	m.lockSlow()
}
```

首先通过CAS来尝试获取锁，如果mutexLocked不是0就调用`sync.Mutex.lockSlow`尝试通过自旋来获取锁，分为几个步骤：

- 1.首先判断能否进入自旋状态

- 2.通过自旋等待锁的释放

- 3.计算锁的最新状态

- 4.更新锁的状态并获取锁

能够进入自旋状态需要满足几个条件：

- 1.互斥锁必须在`正常模式`

- 2.运行在`多CPU`的机器上

- 3.自旋次数`小于4次`

- 4.至少存在一个`运行的处理器P`并且运行队列为空

**个人理解**：lockSlow整体是一个很大的for循环，如果可以进入自旋状态就不必处理后续的锁状态更新等操作，所以`自旋的开销更小`

处理了自旋之后，就计算锁的状态并通过CAS尝试获取锁并更新状态，如果获取成功，就break跳出整个循环，否则调用`runtime.sync_runtime_SemacquireMutex`，它会不断`尝试获取锁`并陷入休眠`等待信号量的释放`，从而保证锁资源不会被两个goroutine同时获取

### 解锁

解锁通过`sync.Mutex.Unlock`方法实现

```go
func (m *Mutex) Unlock() {
	new := atomic.AddInt32(&m.state, -mutexLocked)
	if new != 0 {
		m.unlockSlow(new)
	}
}
```

它会先调用`sync/atomic.AddInt32`快速解锁，如果返回0，说明解锁成功，否则调用`sync.Mutex.unlockSlow`进行慢速解锁，分为以下几个步骤：

- 1.首先验证互斥锁的合法性，如果`已经被解锁`，就抛出异常

- 2.如果互斥锁在`正常模式`下：

    - 如果互斥锁`不存在等待者`或mutexLocked、mutexStarving、mutexWoken三个标志位`不同时为0`（说明锁被其它人占用），方法直接返回，`不唤醒`其它等待者

    - 如果存在等待者，就`唤醒`等待者并交出锁的控制权

- 3.如果在`饥饿模式`下，就`直接唤醒`一个锁的等待者并交出控制权

## RWMutex

RWMutex（读写锁）是细粒度的互斥锁，它的读锁和读锁之间并不互斥，所以在读多写少的场景下能够有更高的性能
、
### 数据结构

读写锁的数据结构由`sync.RWMutex`定义

```go
type RWMutex struct {
	w           Mutex  // 互斥锁，用于写操作
	writerSem   uint32 // 等待读操作完成的写入方
	readerSem   uint32 // 等待写操作完成的读取方
	readerCount int32  // 正在执行的读操作数量
	readerWait  int32  // 写操作被阻塞时等待的读操作个数
}
```

### 写锁

写锁的获取通过`sync.RWMutex.Lock`方法，有三个步骤：

- 1.阻塞后续的`写`操作

- 2.阻塞后续的`读`操作（通过将readerCount变成`负数`）

- 3.如果当前有未完成的读操作，当前goroutine会进入`休眠`状态等待所有读操作完成释放`writerSem信号量`来唤醒

写锁的释放通过`sync.RWMutex.Unlock`实现，它的逻辑与获取写锁刚好相反：

- 1.释放`读锁`（通过将readerCount变回正数）

- 2.`唤醒`所有因为获取读锁而等待的goroutine

- 3.释放`写锁`

获取锁的时候`先锁住写操作`，后锁住读操作，释放锁的时候`先释放读操作`，后释放写操作，这样能够避免读操作被连续的写操作`饿死`

### 读锁

读锁的加锁通过`sync.EWMutex.RLock`实现，它会调用`sync/atomic.AddInt32`方法将`readerCount加1`，如果AddInt32()返回`负数`，说明其它goroutine正在占有写锁，当前goroutine陷入`休眠`，否则成功返回

读锁的解锁通过`sync.RWMutex.RUnlock`实现，它调用`sync/atomic.AddInt32`方法将`readerCount减1`，如果AddInt32()返回`非负数`，说明解锁成功，直接返回，否则要调用`sync.RWMutex.rUnlockSlow`，它会减少readerWait，并在所有读操作都被释放后（`readerWait为0`时）触发写操作的信号量writerSem，唤醒尝试获取写锁的goroutine

## WaitGroup

WaitGroup用于等待一组goroutine的返回，实现`批量的并发`

### 数据结构

`sync.WaitGroup`的数据结构：

```go
type WaitGroup struct {
	noCopy noCopy     // 保证WaitGroup不会被以再赋值的方法拷贝
	state1 [3]uint32  // 状态和信号量
}
```

nocopy的作用是检查WaitGroup是否使用了`值传递`的方式，如果使用值传递，state1会被复制，但对应的信号量不会被复制，所以通过值传递复制出的新WaitGroup是不可用的，此时会报错

state1是一个存储WaitGroup状态和信号量的数组，在64位系统和32位系统中它的结构有所区别

[![cHMLB6.png](https://z3.ax1x.com/2021/04/20/cHMLB6.png)](https://imgtu.com/i/cHMLB6)

waiter用于WaitGroup.Wait的计数

counter用于WaitGroup.ADD和WaitGroup.Done的计数

sema用于信号量的唤醒和等待

### 接口

WaitGroup的使用主要是通过它对外暴露的三个接口来实现的: `WaitGroup.Wait`, `WaitGroup.Done`和`WaitGroup.ADD`

ADD会将counter`加1`只有当`counter为0`的时候才会唤醒处于等待状态的goroutine，Done是向ADD方法`传入了-1`

Wait会在`counter大于0`，且当前WaitGroup`没有被重复使用`的时候（重复使用会报错），将当前goroutine陷入`休眠`
