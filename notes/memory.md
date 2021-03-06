## 物理内存与虚拟内存

[参考1](https://mp.weixin.qq.com/s/xej6klx2q0G1fp82_vKCOg)

[参考2](https://sylvanassun.github.io/2017/10/29/2017-10-29-virtual_memory/)

虚拟内存是围绕进程产生的

虚拟内存为进程提供了一致的、私有的地址空间，每个进程都认为自己在`独享主存`

虚拟内存将主存看成磁盘的高速缓存，将不连续的物理地址映射到了`连续的虚拟地址`上，为程序编写带来了便利

虚拟内存的大小为`2^计算机位数`

每个进程都有独立的虚拟地址空间，保存在页表中，页表保存在`高速缓存或主存中`

页表是页表条目(Page Table Entry PTE)的集合，每次CPU进行虚拟寻址时，都需要通过内存管理单元(Memory Management Unit MMU)结合页表来将虚拟地址`翻译`成物理地址

页表默认每一页`4KB`，每一条PTE`4字节`，每个PTE映射一个`4MB的片`

页命中和缺页（页不命中，在主存中选择牺牲页）

- 二级页表优点：分级之后，如果一级页表的条目为空，二级页表就`不必存在`，且二级页表不必存在主存中，可以在`需要时被创建`