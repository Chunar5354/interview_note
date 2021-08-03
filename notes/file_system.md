## 关于文件的三个数据结构

- 在每个进程中，会维护一个当前进程的`文件描述符表`，它的索引是文件描述符（整数），值是对应的文件在系统级打开文件表中的`位置`

- 在操作系统中，内核会为所有打开的文件维护一个`系统级`的`打开文件表`，它里面真正存储了文件的所有信息，包括文件的偏移量，状态，访问模式（读写）以及i-node的指针等

- i-node相当于实际的文件（元信息），它存储在磁盘上，存储的信息包括文件的字节数，User ID，Group ID，权限，时间戳，链接数（有多少文件名指向这个i-node），文件数据块在磁盘上的位置等

如图所示

[![fS7XYF.md.png](https://z3.ax1x.com/2021/08/02/fS7XYF.md.png)](https://imgtu.com/i/fS7XYF)

## i-node

[参考](https://www.ruanyifeng.com/blog/2011/12/inode.html)

在硬盘格式化的时候，操作系统自动将硬盘分为两个区域，实际的`文件数据区`和`i-node区`

通常每个i-node节点占128或256字节，在磁盘上每隔1KB或2KB设置一个i-node

可以通过`df -i`查看每个硬盘分区的i-node信息

```
$ df -i
Filesystem      Inodes  IUsed   IFree IUse% Mounted on
udev            234983    338  234645    1% /dev
tmpfs           239004    623  238381    1% /run
/dev/vda1      2621440 448122 2173318   18% /
tmpfs           239004      7  238997    1% /dev/shm
```

使用下面的命令来查看i-node大小

```
$ sudo dumpe2fs -h /dev/vda1 | grep "Inode size"
dumpe2fs 1.44.5 (15-Dec-2018)
Inode size:	          256
```

注意当i-node用完时，在磁盘上就无法创建新文件

可以通过`stat`命令查看文件的信息

```
$ stat test1
  File: test1
  Size: 0         	Blocks: 0          IO Block: 4096   regular empty file
Device: fe01h/65025d	Inode: 656173      Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1001/  chunar)   Gid: ( 1001/  chunar)
Access: 2021-06-29 10:13:55.684460392 +0800
Modify: 2021-06-29 10:13:55.684460392 +0800
Change: 2021-06-29 10:13:55.684460392 +0800
```

上面的`Inode: 656173`表示test1这个文件的i-node号码为656173，还可以通过`ls -i`来查看i-node号码

```
$ ls -i test1
656173 test1
```

在操作系统内部，识别文件不是依赖文件名，而是`依赖i-node号码`

所以在用户通过文件名打开文件时，系统首先要根据文件名找到文件的i-node号，然后根据i-node号获取i-node信息，然后再从i-node信息中得到文件数据所在的block，读出数据

文件名与i-node的映射是通过`链接`来实现的，链接分为硬链接与软链接

- 硬链接是将多个文件名指向同一个i-node，对文件内容的`修改会影响`到所有的文件名，`删除一个文件名不影响`其他文件名，但每删除一个文件名。i-node的链接数就减一（对应stat中的Links字段），当链接数为0时，这个i-node就会被系统回收

通过`ln`来实现硬链接：

```
ln 源文件 目标文件
```

- 软链接

假设文件B有一个软链接文件A，则A与B实际指向的`不是同一个i-node`，但是文件A的内容是指向文件B的路径，在读取文件A时，系统会自动定向到文件B

如果删除了B再访问A时，打开文件A就会报错，相当于文件A指向的是文件B的文件名，而不是文件B实际的i-node

软链接通过`ln -s`实现：

```
ln -s 源文件 目标文件
```
