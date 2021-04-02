## 数组

数组是相同类型元素的集合，在内存上是连续的

go中数组的类型由`元素类型`和`数组长度`标识，也就是说即使元素类型相同，但数组长度不同的两个数组也会被认为是不同类型

数组初始化有两种方式：

```go
arr1 := [3]int{1, 2, 3}
arr2 := [...]int{1, 2, 3}
```

对于第二种，go会先推断出数组的长度，实际应用时二者没有区别

当数组元素`小于等于4`个时，直接将数组元素放在`栈`上，当数组元素`大于4`个时，会将元素放在`静态区`，在运行时取出

go数组在`编译期间`就会转换成直接读写内存，并插入`运行时方法`来判断是否发生越界

## 切片

切片的长度是可变的

Slice类型由三个属性：

```go
type SliceHeader struct {
	Data uintptr
	Len  int
	Cap  int
}
```

Data是指向切片元素的指针（指向一块连续的内存空间），Len是切片的长度，Cap是切片的容量

如果在创建切片时不指定cap，则默认cap`等于len`

切片在`运行时`才能确定内容与结构，申请的内存大小等于`元素大小 × 切片容量`

### 切片的扩容

当切片中元素逐渐增多时，原来的容量不够，就需要扩容

扩容操作通过`runtime.growslice`函数来实现，它接收一个期望容量参数，扩容时有以下几种策略：

- 1.如果期望容量`大于原来容量的2倍`，就扩容成期望容量

- 2.期望容量小于原来容量的2倍，原来切片的`长度小于1024`，就将容量`翻倍`

- 3.期望容量小于原来容量的2倍，原来切片的长度`大于等于1024`，就每次增加`1/4`的容量，知道新容量大于原来的容量

确定了切片的容量之后，会根据切片中元素的大小`对齐内存`，对齐时根据`runtime.class_to_size`数组的元素向上取整(只会取到数组内的值)

```go
var class_to_size = [_NumSizeClasses]uint16{
    0,
    8,
    16,
    32,
    48,
    64,
    80,
    ...,
}
```

### 切片逃逸

go语言中的变量携带一组校验数据，用来验证它的整个生命周期是否在`运行时完全可知`，如果校验通过，这个变量就在`栈上`分配，否则就称这个变量`逃逸`了，就在`堆上`分配

内存逃逸有以下几种典型情况：

- 1.对于slice，当slice中存储指针类型时，其引用的值可能在堆上

- 2.由于slice有可能需要扩容，所以当slice的存储要基于运行时数据进行扩容时，就需要在堆上分配

- 3.在函数内部返回局部变量的指针，由于变量被外部引用，所以生命周期大于栈

- 4.发送指针或带指针的值到channel中，此时无法判断这个channel将在那个doroutine被读取，所以也要分配在堆上

- 5.在interface类型上调用方法，这是动态的实现，方法的具体实现方式要在运行时在能知道