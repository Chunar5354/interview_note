[参考](https://draveness.me/golang/docs/part2-foundation/ch04-basic/golang-reflect/#43-%E5%8F%8D%E5%B0%84)

Go的反射reflect主要用来获取运行时变量的`类型`（reflect.Type）和`值`（reflect.Value）

## Go反射的三大法则

- 1.只能从interface{}对象得到反射对象

因为Go的函数调用都是值传递，所以在调用`reflect.TypeOf()`和`reflect.ValueOf()`时会自动将传入的变量转换为interface{}类型

- 2.反射对象只能获取到interface{}对象

使用ValueOf获取的对象类型是reflect.Value，可以通过`reflect.Value.Interface()`方法转换成原始类型

```go
v := reflect.ValueOf(1)
vi := v.Interface()
fmt.Printf("%T, %T", v, vi)

// reflect.Value, int
```

- 3.如果要修改反射对象，其值必须是可设置的

使用反射是不能对原变量进行修改的，会引发unaddressable错误

```go
var a int
v := reflect.ValueOf(a)
v.SetInt(3)
fmt.Println(a)

// panic: reflect: reflect.Value.SetInt using unaddressable value
```

如果要修改的话，只能获取原变量的`指针的反射`，并通过`reflect.Value.Elem()`获取指针指向的变量并修改

```go
var a int
v := reflect.ValueOf(&a)
v.Elem().SetInt(3)
fmt.Println(a)

// 3
```
