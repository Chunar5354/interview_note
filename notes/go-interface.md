[参考](https://draveness.me/golang/docs/part2-foundation/ch04-basic/golang-interface/)

使用接口可以使得上层模块和下层模块之间互相`解耦`，上层的模块只需要实现一个约定好的接口，而不需要依赖下层模块

Go中的接口是`隐式`接口，即只要一个对象实现了接口中定义的所有方法，这个对象就实现了这个接口，不需显式指定

Go中使用`runtime.iface`表示带有方法的接口，使用`runtime.eface`表示空接口`interface{}`

### 类型问题

假设有一个接口和一个类型：

```go
type ppp interface {
	Print()
}

type Ppp struct {
}
```

要想为类型Ppp实现接口ppp，可以有两种方法：

```go
func (p Ppp) Print() {
	fmt.Println("ok")
}

func (p *Ppp) Print() {
	fmt.Println("ok")
}
```

注意这两种方法不能同时出现，否则会报错：

```
method redeclared: Ppp.Print
        method(Ppp) func()
        method(*Ppp) func()
```

相应的，调用接口的方法也有两种方式：

```go
// 通过结构体调用
var p ppp = Ppp{}
p.Print()
// 通过指针调用
var p ppp = &Ppp{}
p.Print()
```

其中只有`通过结构体来调用指针的方法`是不可行的，详细说明可以参考：[指针可以隐式获取到指向的结构体](https://draveness.me/golang/docs/part2-foundation/ch04-basic/golang-interface/#%E6%8C%87%E9%92%88%E5%92%8C%E6%8E%A5%E5%8F%A3)

### 非空接口

非空接口的数据类型为`runtime.iface`:

```go
type iface struct { // 16 字节
	tab  *itab
	data unsafe.Pointer  // 数据实体
}
```

其中itab的类型为`runtime.itab`:

```go
type itab struct { // 32 字节
	inter *interfacetype  // 表示类型
	_type *_type          // 表示类型
	hash  uint32          // 用于类型转换时快速判断与目标类型是否一致
	_     [4]byte
	fun   [1]uintptr      // 动态派发的虚函数表
}
```

### 空接口interface{}

#### 数据结构

空接口的数据类型为`runtime.eface`:

```go
type eface struct { // 16 字节
	_type *_type          // 类型
	data  unsafe.Pointer  // 数据实体
}
```

#### 空接口不等于任意类型

向空接口进行隐式类型转换时，转换后的变量不仅包含转换之前的变量，还包含转换之前的`类型`

```go
func main() {
	var x interface{} = nil
	var y *int = nil
	interfaceIsNil(x)
	interfaceIsNil(y)
}

func interfaceIsNil(x interface{}) {
	fmt.Printf("%T, %v\n", x, x)
	fmt.Println(x == nil)
}
```

结果：

```
<nil>, <nil>
true
*int, <nil>
false
```

可以看到转换后的变量y并不是nil，所以接口类型并`不是任意类型`