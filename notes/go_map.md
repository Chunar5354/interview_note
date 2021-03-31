go中map的实现原理

[参考1](https://zhuanlan.zhihu.com/p/66676224)

[参考2](https://draveness.me/golang/docs/part2-foundation/ch03-datastructure/golang-hashmap/#%E5%86%99%E5%85%A5)

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

一些比较重要的属性：

count是哈希表中键值对的数量

B代表bucket的数量（`2^B`个）

buckets是外链法中指向bucket的指针

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
    topbits  [8]uint8    // 一个数组，存储每个键哈希值的高8位
    keys     [8]keytype  // 每个bucket最多只存储8个键值对
    values   [8]valuetype
    pad      uintptr
    overflow uintptr    // 指向扩容桶的指针，即外链的下一个节点
}
```

go中每个bucket最多存储`8个键值对`，冲突元素很多时需要`扩容`


### 定位key的步骤

- 1.根据哈希函数计算出key的哈希值，用哈希值的`低B位`来找到key存储在`哪个buckets`（哪条外链）

- 2.将哈希值的`高8位`与bmap的`tophash`属性比较，得到key具体在`哪个bucket`中（外链的哪个节点）

- 3.得到了key所在的bucket，还要完整的判断key是否相等（不能只是高8位了）

### 扩容

在go中有两种情况需要对哈希表扩容：

- 1.装载因子超过阈值，默认是`6.5`(装载因子等于键值对数/桶数，即`count/2^B`)，因为每个桶有8个元素，所以装载因子最大值时8，当达到6.5时说明桶已经很满了

- 2.溢出桶（overflow bucket）的数量过多，这里也分两种情况：当`B<15`时，溢出桶数量超过`2^B`就扩容；当`B>=15`时，溢出桶数量超过`2^15`就扩容。有可能是先插入再删除产生了很多`空桶`，但未达到装载因子的阈值，在这种情况下，key分布的很分散，而且由于外链的overflow bucket很多，链表的查找复杂度是`O(n)`，就导致效率很低

对于以上两种情境，有不同的策略

- 如果是由于装载因子达到阈值，说明此时键值对太多，而bucket不够，此时会开辟新的buckets空间，将旧的buckets指向hmap的`oldbuckets`，新的buckets大小为旧空间的`2倍(2*2^B)`

- 如果是由于overflow bucket过多，说明此时键值对并不多，而是bucket有冗余，此时开辟一个`大小相等`的新buckets空间，在新空间中key会排列的更紧密

注意在扩容时调用的函数是`hashGrow()`，此时只是分配了新空间，而旧空间的键值对并`没有移动`到新空间（因为一次性移动所有元素性能很差）

旧元素的移动发生在`写入和删除`操作时，在写入(mapassign)和删除(mapdelete)函数中都有一个`if h.growing()`的判断（其实是判断`oldbuckets`指针是否为空），当正在扩容时，就会调用`growWork()`进行数据迁移，而growWork()实际上是调用了`evacuate()`函数，真正的迁移操作发生在evacuate()中，看看growWork()的代码：

```go
func growWork(t *maptype, h *hmap, bucket uintptr) {
	// make sure we evacuate the oldbucket corresponding
	// to the bucket we're about to use
	evacuate(t, h, bucket&h.oldbucketmask())

	// evacuate one more oldbucket to make progress on growing
	if h.growing() {
		evacuate(t, h, h.nevacuate)
	}
}
```

growWork会调用evacuate()一到两次，所以每次只能迁移`一个或两个数据`

对于等量bucket迁移，新旧key会落在同一个位置，而对于2倍迁移，由于B增加了，由哈希值算出的bucket位置也会改变，所以map是`无序的`

### 遍历

Go在遍历map时，会从一个`随机的初始bucket`开始遍历，所以更增加了随机性

遍历过程中也会遇到扩容问题，需要检查`标志位`来判断该数据是否被迁移过，如果迁移过，就按新的buckets序号顺序（bmap构成的数组），如果还没被迁移，就到旧buckets中找到对应的key，并且计算这些key有多少落在新buckets的当前中，然后再按顺序遍历新buckets

注意`始终都在按顺序遍历新buckets`，只是在遇到未迁移数据时要到旧buckets中找哪些key将要迁移到新buckets的当前位置

### 总结

- go map基础结构是使用外链法的哈希表

- 两个主要结构：hmap是哈希表，bmap是外链桶

- 哈希值的低B位用于寻找bucket，高8位用于查找bucket中的key，每个bucket有8个元素

- 装载因子过大或桶溢出会导致扩容，扩容有等量扩容和2倍扩容，扩容只分配空间，数据移动发生在写入和删除操作
