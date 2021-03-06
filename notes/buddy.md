程序在运行过程中经常要申请和释放内存空间，如果对内存管理不当，就可能导致产生大量的内存碎片，浪费资源

伙伴算法是一种解决内存碎片问题的有效方法

## 伙伴算法

伙伴算法的基本思想是将内存分成`大小不同的块`，然后在分配时分配`大于所需内存的最小内存块`，并`向下分裂`，同时在回收内存时`向上合并`

使用伙伴算法可以完全解决`外部碎片`

下面做详细的说明：

在Linux系统中，将所有的空闲内存分为11个链表，每个链表分别对应大小为1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024的`页框`（页框就是有多少个页，比如页框为4，那这个内存单元就有4个页，`4*4k字节`

举个例子，假设有下面的内存：

[![hAQCk9.png](https://z3.ax1x.com/2021/08/24/hAQCk9.png)](https://imgtu.com/i/hAQCk9)

此时要申请一块16页的内存，则会选中大小为32的页框分配出去，同时将剩下的一半变成长度16的页框，`加入16的链表`

[![hAQakj.png](https://z3.ax1x.com/2021/08/24/hAQakj.png)](https://imgtu.com/i/hAQakj)

接下来要分配一块25页的内存，则会选中64的页框，同时由于25小于64的一半，此时会将64平分为两个32，将其中一个32分配出去（注意此时产生了`内部碎片`），另一个`加入32的链表`

[![hAQIc6.png](https://z3.ax1x.com/2021/08/24/hAQIc6.png)](https://imgtu.com/i/hAQIc6)

注意到在分配内存时会产生分裂，分裂后的两部分内存块就称为`伙伴`，一对伙伴需要满足下面的条件：

- 1.两个伙伴具有相同大小的页框n

- 2.两个伙伴的内存地址连续

- 3.第一个伙伴的内存起始地址是`n*2*4k`（这样才能合并成一个大块）

在内存释放是，如果两个伙伴都是空闲块，就会被合并成一个大块，比如在上面的例子中，如果25页的内存被释放了，两个32就会被重新合并成64（但是不会合并成128，因为起始地址不满足）

## slab算法

伙伴算法是基于页的大块内存管理，在分配小于4k的内存时，显得有些大材小用

所以在伙伴算法的基础上，另外实现了slab算法，它可以实现管理`任意大小的内存`（通常用于小对象）

slab算法的基本思想是`专门`为某一类对象`预先申请`一定的内存空间备用，当需要为这个对象分配内存的时候，就可以迅速从预备好的区域中拿出一块内存使用

通常在满足以下条件的场合才使用slab算法：

- 1.需要`频繁`分配和释放内存

- 2.对象的大小`固定`

场合距离：内核中的文件描述符、进程ID、索引节点等

Linux`内核`中有一个`slab层`，它根据不同的对象分为相应的`高速缓存组`，每个高速缓存组专门用来分配某一类对象，然后每个高速缓存再被划分成slab，每个slab由物理`连续`的一个或多个页组成

每个slab有三种状态：`满、部分满和空`，当有新对象要分配时，优先从部分满的slab中分配

slab的结构如图所示：

[![hAYxIO.png](https://z3.ax1x.com/2021/08/24/hAYxIO.png)](https://imgtu.com/i/hAYxIO)
