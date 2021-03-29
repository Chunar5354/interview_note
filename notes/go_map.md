go中map的实现原理

go的map是由哈希表实现的，采用`外链法`扩容，主要有两种数据结构：hmap和bmap

### 基础结构

- hmap

hmap就是哈希表，下面是go中hmap类型的全部属性：

```go
// A header for a Go map.
type hmap struct {
	// Note: the format of the hmap is also encoded in cmd/compile/internal/gc/reflect.go.
	// Make sure this stays in sync with the compiler's definition.
	count     int // # 元素个数，live cells == size of map.
	flags     uint8
	B         uint8  // 当前哈希表的buckets数量 (can hold up to loadFactor * 2^B items)
	noverflow uint16 // approximate number of overflow buckets; see incrnoverflow for details
	hash0     uint32 // hash seed

	buckets    unsafe.Pointer // 指向bucket数组的指针，array of 2^B Buckets. may be nil if count==0.
	oldbuckets unsafe.Pointer // 扩容时用于复制的指针
	nevacuate  uintptr        // progress counter for evacuation (buckets less than this have been evacuated)

	extra *mapextra // 用于扩容的指针
}
```

其中buckets就是外链法中指向bucket的指针

- bmap

bmap时外链法中存储冲突数据的“桶”，结构如下：

```go
type bmap struct {
	tophash [bucketCnt]uint8  // 存储键哈希值的高8位
}
```

但在运行期间，bmap不只包含一个属性，完整的bmap应该是这样的：

```go
type bmap struct {
    topbits  [8]uint8    // 键哈希的高8位
    keys     [8]keytype  // 每个bucket最多只存储8个键值对
    values   [8]valuetype
    pad      uintptr
    overflow uintptr    // 指向扩容桶的指针
}
```

go中每个bucket最多存储`8个键值对`，冲突元素很多时需要`扩容`


### 定位key的步骤

- 1.根据哈希函数计算出key的哈希值，用哈希值的`低B位`来找到key存储在`哪个buckets`（哪条外链）

- 2.将哈希值的`高8位`与bmap的`tophash`属性比较，得到key具体在`哪个bucket`中（外链的哪个节点）

- 3.得到了key所在的bucket，再逐个进行`全部位`的比对（不能只是高8位了）

### 扩容