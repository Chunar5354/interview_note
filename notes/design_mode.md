[参考](https://lailin.xyz/post/go-design-pattern.html)

设计模式相当于一些编写代码的通用解决方案

设计模式是前人经验的总结，种类很多，下面简单介绍几种常用的设计模式以及Go语言的简单实现

## 单例模式

在整个程序中一个类仅有`一个实例`

- 优点：减少内存的开销以及频繁的创建和销毁实例

- 缺点：没有接口，不能继承，扩展性较差

单例模式分为懒汉式和饿汉式

- 饿汉式：在`类加载`的时候实例就已经创建好(不需要加锁，不支持延迟加载，并发安全)

- 懒汉式：在`第一次调用`实例的时候实例才被创建(需要加锁，延迟加载，并发布安全)

### 代码实例

- 饿汉式

```go
type Single struct{}

var single *Single    // 只有一个全局的实例

func init() {
    single = &Single{}   // 在初始创建，以后获取的都是同一个实例
}

func getSingle() {
    return single
}
```

- 懒汉式

```go
import "sync"

type LazySingle struct{}

var lazySingle *LazySingle

func getLazySingle() {
    if laztSingle == nil {     // 检测是否已存在
        sync.Once.Do(func() {  // 加锁
            lazySingle = &LazySingle{}
        })
    }
    return lazySingle
}
```

## 工厂模式

不对外暴露具体的创建逻辑，客户端使用同一个接口根据条件来创建不同的实例

### 代码实例

假设有一个工厂，生产牛奶和果汁，我们可以通过一个通用的接口来供用户选择是生产牛奶还是果汁，而不向用户展示牛奶和果汁的具体生产细节：

```go
// 通用的工厂接口
type Factory interface {
	Run()
}

// 生产牛奶
type Milk struct {
}

func (m Milk) Run() {
	fmt.Println("This is milk")
}

// 生产果汁
type Juice struct {
}

func (j Juice) Run() {
	fmt.Println("This is juice")
}

// 向用户暴露的统一生产方法
func NewFactory(product string) Factory {
	switch product {
	case "milk":
		return Milk{}
	case "juice":
		return Juice{}
	}
	return nil
}
```

用户只需要这样调用：

```go
func main() {
	m := NewFactory("milk")
	j := NewFactory("juice")
	m.Run()
	j.Run()
}
```

## 建造者模式

使用一系列简单对象一步步构建成一个复杂的对象

适用于构建一个属性很多的类，将每个属性的设置都拆分开来

```go
// 要创建的学生对象
type Student struct {
	Id    string
	Name  string
	Major string
	Class string
	Age   int
}

// 学生对象的builder
type StudentBuilder struct {
	Id    string
	Name  string
	Major string
	Class string
	Age   int
}

// 每个属性各自的构建方法
func (s *StudentBuilder) SetId(id string) *StudentBuilder {
	s.Id = id
	return s
}

func (s *StudentBuilder) SetName(name string) *StudentBuilder {
	s.Name = name
	return s
}

func (s *StudentBuilder) SetMajor(major string) *StudentBuilder {
	s.Major = major
	return s
}

func (s *StudentBuilder) SetClass(class string) *StudentBuilder {
	s.Class = class
	return s
}

func (s *StudentBuilder) SetAge(age int) *StudentBuilder {
	s.Age = age
	return s
}

// 可以根据不同的需要改变这个构建student的方法，如某些属性可能不需要填写或可以填写默认值
func NewStudent() Student {
	s := StudentBuilder{}
	s.SetId("0101").SetName("Bob").SetMajor("CS").SetClass("1801").SetAge(20)
	student := Student{
		Id:    s.Id,
		Name:  s.Name,
		Major: s.Major,
		Class: s.Class,
		Age:   s.Age,
	}
	return student
}
```