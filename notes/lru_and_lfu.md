LRU(Least Recently Used 最久为使用)和LFU(Least Frequently Used 最近最少使用)是两种重要的缓存淘汰策略

本文是这两种算法的Go代码实现

## LRU

[leetcode 146](https://leetcode.com/problems/lru-cache/)

LRU中会设置一个缓存长度，表示最多能缓存多少元素

LRU主要有两个操作：Get()返回最近使用的元素，Put()写入元素，而且在超过缓存长度时要`删除`最久未使用的元素，这就要求对元素进行排序

为了使Get和Put都达到O(1)的复杂度，排序不能用常规的链表来实现，通常是使用`哈希表+双向链表`来实现LRU的数据结构

代码如下所示

```go
// LRU的整体数据结构
type LRUCache struct {
    Cap int                    // 设定的容量
    Length int                 // 当前长度
    Head *DoubleList           // 双向链表的头指针
    Tail *DoubleList           // 双向链表的尾指针
    Map map[int](*DoubleList)  // map的键是指定存储的key，值是双向链表中的节点
}

// 双向链表节点数据结构
type DoubleList struct {
    Key int
    Val int           // 存储的值放在双向链表节点中
    Prev *DoubleList
    Next *DoubleList
}

// 删除一个节点
func remove(n *DoubleList) {
    n.Prev.Next, n.Next.Prev = n.Next, n.Prev
}

// 每次Get或Put时，都要将那个节点更新到双向链表的头部
func (lru *LRUCache) addFirst(n *DoubleList) {
    n.Next = lru.Head.Next
    n.Next.Prev = n
    lru.Head.Next = n
    n.Prev = lru.Head
}

// 当超出缓存容量时，需要将尾部（最久未使用）的节点删除
func (lru *LRUCache) removeLast() {
    lru.Tail.Prev, lru.Tail.Prev.Prev.Next = lru.Tail.Prev.Prev, lru.Tail
}

// 初始化LRU
func Constructor(capacity int) LRUCache {
    // 初始化时为头结点和为节点设置两个虚拟节点
    head := &DoubleList{Key:0, Val:0}
    tail := &DoubleList{Key:0, Val:0}
    head.Next = tail
    tail.Prev = head
    lru := LRUCache{Cap: capacity, Head: head, Tail: tail, Map: make(map[int](*DoubleList))}
    return lru
}

// LRU的Get操作
func (lru *LRUCache) Get(key int) int {
    // 没有需要的内容，返回-1
    if _, ok := lru.Map[key]; !ok {
        return -1
    }
    val := lru.Map[key].Val
    // 查到内容后通过Put更新节点
    lru.Put(key, val)
    return val
}

// 写入节点
func (lru *LRUCache) Put(key int, value int)  {
    if n, ok := lru.Map[key]; ok {
        remove(n)  // 如果已存在就将原来的节点先删除再移到第一个
        lru.Length--
    } else {
        if lru.Length == lru.Cap { // 超过长度时删除最后一个节点
            // 注意必须先删除map再删除链表的节点，因为如果先删除了链表的尾节点在map里面就定位不到了
            delete(lru.Map, lru.Tail.Prev.Key)
            lru.removeLast()
            lru.Length--
        }
    }
    // 为当前键值对新建一个节点并插入到头部
    node := &DoubleList{Key: key, Val: value}
    lru.Map[key] = node
    lru.addFirst(node)
    lru.Length++
}
```

有几点需要注意的地方：

- 1.双向链表有三个操作：remove, addFirst和removeLast

- 2.在LRU的数据结构中保存双向链表的头结点和尾节点，并在初始化时为它们创建虚拟指针

- 3.LRU的map中存储的是双向链表的节点，这样就能实现O(1)查找

- 4.删除尾节点时通过双向链表的尾指针来定位map中的元素，而且要注意删除顺序

## LFU

[leetcode 460](https://leetcode.com/problems/lfu-cache/)

[参考](https://cloud.tencent.com/developer/article/1645636)

LFU要复杂一些，因为要为每个节点维护频率属性，在多个频率相同的情况下则要遵循LRU原则

依然是使用`哈希表+双向链表`来实现O(1)的操作，不过在LFU中需要`两个嵌套的双向链表`，如下图所示：

[![cAUsy9.md.png](https://z3.ax1x.com/2021/03/31/cAUsy9.md.png)](https://imgtu.com/i/cAUsy9)

水平链表按照`频率减小`的顺序排序，每个水平链表的节点还含有一个垂直节点，表示具有`相同频率的键值对`，垂直链表根据LRU原则，将最近使用的节点排在链首，所以按照上面的图示左上角的垂直节点是使用频率最高且最近使用的，右下角的节点是使用频率最低且最近未使用的

哈希表的值指向垂直节点，垂直节点中也包含一个属性指向`它所属于的水平节点`

代码实现：

```go
type LFUCache struct {
    Cap int
    Length int
    Head *HDoubleList
    Tail *HDoubleList
    Map map[int](*VDoubleList)
}

// 水平链表
type HDoubleList struct {
    Freq int
    Prev *HDoubleList
    Next *HDoubleList
    VHead *VDoubleList
    VTail *VDoubleList
}

// 垂直链表
type VDoubleList struct {
    Freq int
    Key int
    Val int
    Prev *VDoubleList
    Next *VDoubleList
    HDL *HDoubleList  // 当前垂直节点所属的水平节点
}

// 根据频率创建水平节点
func ConstructHDL(freq int) HDoubleList {
    vhead := &VDoubleList{Freq:0}
    vtail := &VDoubleList{Freq:0}
    vhead.Next = vtail
    vtail.Prev = vhead
    hdl := HDoubleList{Freq:freq, VHead:vhead, VTail:vtail}
    return hdl
}

// 创建LFU
func Constructor(capacity int) LFUCache {
    head := &HDoubleList{Freq:0}
    tail := &HDoubleList{Freq:0}
    head.Next = tail
    tail.Prev = head
    lfu := LFUCache{Cap:capacity, Head:head, Tail:tail, Map:make(map[int](*VDoubleList))}
    return lfu
}

// 向水平链表中添加节点
func addHdl(prev, curr *HDoubleList) {
    curr.Next = prev.Next
    curr.Next.Prev = curr
    curr.Prev = prev
    prev.Next = curr
}

// 向垂直链表添加节点
func addVdl(prev, curr *VDoubleList) {
    curr.Next = prev.Next
    curr.Next.Prev = curr
    curr.Prev = prev
    prev.Next = curr
}

// 删除垂直节点
func removeVdl(vdl *VDoubleList) {
    vdl.Prev.Next, vdl.Next.Prev = vdl.Next, vdl.Prev
}

// 删除水平节点
func removeHdl(hdl *HDoubleList) {
    hdl.Prev.Next, hdl.Next.Prev = hdl.Next, hdl.Prev
}

// LFU读取
func (lfu *LFUCache) Get(key int) int {
    if _, ok := lfu.Map[key]; !ok {
        return -1
    }
    vdl := lfu.Map[key]
    val := vdl.Val
    freqInc(vdl) // 为当前垂直节点增加频率
    return val
}

// LFU写入
func (lfu *LFUCache) Put(key int, value int)  {
    if vdl, ok := lfu.Map[key]; ok {
        vdl.Val = value
        freqInc(vdl)  // 增加当前节点频率
    } else {
        // 超过容量要先删除
        if lfu.Length == lfu.Cap {
            // 水平链表的频率从前往后逐渐降低
            // 垂直链表将最近使用的节点放在头部
            // 因此最低频率且最近未使用的节点是lfu.Tail.Prev.Vtail.Prev
            toDelete := lfu.Tail.Prev.VTail.Prev
            delete(lfu.Map, toDelete.Key)
            removeVdl(toDelete)
            lfu.Length--
            if toDelete.HDL.VHead.Next.Next == nil {  // 说明当前水平节点对应的垂直链表空了，此时要删除这个水平节点
                removeHdl(toDelete.HDL)
            }
        }
        // 新建一个节点
        vdl := &VDoubleList{Freq:1, Key:key, Val:value}
        lfu.Map[key] = vdl
        lfu.Length++
        LastHdl := lfu.Tail.Prev
        // 判断最后一个节点的频率是否是1
        if LastHdl.Freq == 1 {
            addVdl(LastHdl.VHead, vdl)  // 如果存在就把当前节点添加到它的头部
        } else {
            nh := ConstructHDL(1)   // 如果不存在则要新建一个水平节点
            newHdl := &nh
            addHdl(LastHdl, newHdl)     // 并把这个新建的节点插入到最后
            addVdl(newHdl.VHead, vdl)   // 再将当前垂直节点插入到这个水平节点中
        }
    }
}

// 增加节点频率
func freqInc(vdl *VDoubleList) {
    // 首先将垂直节点从它的水平节点中删除
    removeVdl(vdl)
    prevHdl := vdl.HDL.Prev
    if vdl.HDL.VHead.Next == vdl.HDL.VTail {  // 说明当前水平节点对应的垂直链表空了，此时要删除这个水平节点
        removeHdl(vdl.HDL)
    }
    vdl.Freq++
    // 判断前一个水平节点的频率是否等于当前频率加1
    if prevHdl.Freq == vdl.Freq {
        addVdl(prevHdl.VHead, vdl)  // 等于就添加到头部
    } else {
        nh := ConstructHDL(vdl.Freq)  // 如果不等于则要新建一个水平节点
        newHdl := &nh
        addHdl(prevHdl, newHdl)     // 并把这个新建的节点插入到中间
        addVdl(newHdl.VHead, vdl)   // 再将当前垂直节点插入到这个水平节点中
    }
}
```

要点：

- 1.LFU需要借助哈希表和两个互相`嵌套`的双向链表来实现O(1)的操作

- 2.在进行Put和Get操作时都要对节点频率进行增加
