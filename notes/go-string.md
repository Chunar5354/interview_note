Go中的字符串是一个`只读`的`字节数组`在运行时可以表示为`reflect.StringHeader`

```go
type StringHeader struct {
	Data uintptr  // 指向数组的指针
	Len  int      // 数组长度
}
```

string类型与[]byte类型经常互相转换，区别在于[]byte是可变的

二者互相转换的时候都需要进行`拷贝`，有一定的开销