## shell

shell意为`壳`，是用户与内核进行交互的渠道

### $变量

- `$#`表示参数个数

- `$0`脚本名

- `$1`传给脚本的第一个参数

- `$2`传给脚本的第二个参数

- `$$`脚本运行的当前`进程ID`

- `$?`脚本运行的返回值，当运行成功时值为0，否则为1

### shell命令的返回

shell命令在运行后会返回一个`$?`变量，当运行成功时值为0，否则为1

可以在运行命令后查看

```
$ echo $?
```

## Linux常用shell命令

### 查看cpu信息

```
$ cat /proc/cpuinfo
```

### 查看内存信息

```
$ cat /proc/meminfo
```

或

```
$ free
```

free可以带参数，`-k`, `-m`, `-g`分别表示以KB，MB和GB为单位来表示内存大小

### 查看系统版本

```
$ uname -a
或
$ lsb_release
```

### 查看网络适配器

```
$ ip a
```

### 查看用户

who列出前所用登录的用户信息

```
$ who
chunar   pts/0        2021-05-29 20:23 (123.123.123.123)
```

从左到右：用户名，登陆终端，登陆时间，登录的主机名或IP

或者使用功能更强大的`w`

```
$ w
21:46:03 up 46 days,  5:47,  1 user,  load average: 0.01, 0.03, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
chunar   pts/0    123.123.123.123   20:23    0.00s  0.17s  0.00s w
```

第一行是系统负载相关内容

第二行的各字段：

- USER，用户名

- TTY，登陆终端

- FROM，登录主机名或IP

- LOGIN@，登录时间

- IDLE，从上一次与终端交互以来的空闲时间

- JCPU，在当前TTY上的进程使用的时间

- PCPU，当前进程所使用的时间

- WHAT，当前进程

### 查看系统负载

简单查看：

```
$ uptime
21:24:42 up 46 days,  5:25,  1 user,  load average: 0.04, 0.04, 0.01
```

从左到右分别是当前时间、开机至今运行时间，用户，1，5和15分钟的平均负载

或者也可以通过`w命令`（具体解释见查看用户一节）

```
$ w
21:30:36 up 46 days,  5:31,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
chunar   pts/0    123.123.123.123   20:23    0.00s  0.17s  0.00s w
```


功能最强大：`top`

```
$ top
```

top可以带参数，常用的`-d`表示每隔多少秒刷新一次，`-p`表示查看某个进程PID，`-c`表示显示进程的命令行参数

如

```
$ top -d 3 -c -p 18690
```

top输出中`load average`的含义：在过去1分钟、5分钟和15分钟内的CPU平均负载

如`load average: 0.12 0.22 0.13`表示过去一分钟内在CPU运行或等待运行的`平均进程数`，以此类推，每个CPU同时只能运行一个进程，所以当数字`超过CPU核数`时，说明系统负载过高（通常为核心数*0.7以下）

### 查看IO

#### vmstat

使用方法：

```
vmstat n1(几秒输出一次) n2(一个输出几次)
```

```
$ vmstat
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 4  0      0 192484  56624 473144    0    0    91    36    7    4  1  1 98  0  0
```

参数：

- `r`，等待运行的进程数

- `b`，非中断状态睡眠的进程数

- `swpd`，交换区内存使用情况（KB）

- `free`，可用内存（KB）

- `buff`，缓冲区内存（KB）

- `cache`，缓存区内存（KB）

- `si`，从磁盘交换到内存的数量（KB/s）

- `so`，从内存交换到硬盘的数量（KB/s）

- `bi`，发送到块设备的块数（块/s）

- `bo`，从块设备接受的块数（块/s）

- `in`，每秒中断数

- `cs`，每秒上下文切换数

- `us`，CPU使用率（%）

- `sy`，内核占用CPU（%）

- `id`，可用CPU（%）

- `wa`，等待IO的CPU占用（%）

块大小默认是`4096字节`，可以通过stat命令查看：

```
$ stat -f / | grep block
Block size: 4096       Fundamental block size: 4096
```

#### iostat

iostat属于sysstat，需要先安装：

```
$ spt-get install sysstat
```

会输出CPU和硬盘读写信息：

```
$ iostat -h
Linux 4.19.0-11-amd64 (VM-4-10-debian) 	06/02/2021 	_x86_64_	(1 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.1%    0.0%    0.8%    0.1%    0.0%   98.0%

      tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn Device
     4.09        90.3k        35.6k     372.2G     146.6G vda
     0.00         0.0k         0.0k       1.1M       0.0k scd0
     0.00         0.0k         0.0k     482.0k       0.0k loop0
```

### 查看系统日志

```
$ dmesg
或
$ dmesg | tail   // 只输出日志的最后10行
```

### 查看文件大小

```
$ du
```

du默认会按照字节数打印出当前目录下所有子目录中文件的大小，有更友好的方式

```
$ du -h --max-depth=1
```

`-h`表示human-readable，即用户友好的方式，它会以常用的KB，MB等单位打印出文件大小

`--max-depth=1`表示只统计当前目录下`一层`的文件（文件夹）大小，不会向下深入统计

### 数据流重定向

通过`>`和`<`可以将`标准输入和输出`的数据重定向到`文件`

`>`意为将`标准输出`重定向到文件(`写入`)，如

```
$ ls > test.txt
```

就会在当前目录下新建一个text.txt文件，并将ls的结果写入文件，而不会在命令行中打印结果

`<`意为将`文件`的数据重定向到`标准输入`(`读取`)

如

```
$ cat > test1 < test2
```

就会将test2文件中的内容输入到test1（相当于复制）

从左到右执行，首先遇到`cat > test`，需要将标准输出（默认由`键盘输入`）的值写入到test1文件，然后遇到`< test2`，将test2文件的内容重定向到了标准输入，于是就将test2的内容复制到了test1

`<`与`>`是覆盖模式，会删除文件中原本的内容，如果想要保留文件的内容，可以使用`>>`或`<<`的追加模式，它们会在文件的末尾继续添加内容

### tee将标准输入复制到文件和标准输出

通过`<>`的重定向可以将标准输入重定向到文件，但这种方式不能用在`管道`命令中

可以通过`tee`命令来处理管道中的标准输入

tee可以将标准输入同时复制到`标准输出`和`多个文件`，示例：

```
$ date | tee testfile1 testfile2
Sat 29 May 2021 09:00:55 PM HKT
$ cat testfile1
Sat 29 May 2021 09:00:55 PM HKT
$ cat testfile2
Sat 29 May 2021 09:00:55 PM HKT
```

通过`-a`参数可以像文件中追加内容

### 修改权限

修改文件（文件夹）的权限通过`chmod`实现，如

```
$ chmod 755 testfile
```

那755这三个数字分别代表什么意思呢？

在Linux系统中，文件有三种权限，读（r），写（w）和执行（x），通过`ls -l`命令可以看到

```
$ ls -l | grep test
drwxr-xr-x 2 chunar chunar 4096 May 22 09:11 test
```

其中每一种权限都对应一个`权限数值`，`r=4`, `w=2`, `x=1`，因为都是2的n次方，所以它们任意组队的和都是`唯一的`，所以可以通过数字来表示文件具有哪些权限：

```
7 = 4 + 2 + 1, 权限：rwx
6 = 4 + 2,     权限：rw-
5 = 4 + 1,     权限：r-x
4 = 4,         权限：r--
3 = 2 + 1,     权限：-wx
2 = 2,         权限：-w-
1 = 1,         权限：--x
```

在ls -l命令的输出中，表示权限的字符串为`drwxr-xr-x`，第一个d表示是一个文件夹，后面的rwx组合共有三组，从左到右依次表示`文件所有者`，`群组用户`，`其他用户`所拥有的权限

### 根据条件查找文件

- 指定文件名的范围

```
$ ls ./[a-h]*    // 以a-h开头的文件
$ ls ./[^a-h]*   // 不以a-h开头的文件
```

- 指定文件名的长度

```
$ ls ./????     // 文件名长度为4的文件
```

- 指定文件内容

```
grep 'test' ./*       // 在当前目录下找到包含'test'内容的文件，并打印出所在的行
grep -v 'test' ./*    // 搜索不包含'test'的文件行
grep -i 'test' ./*    // 忽略大小写
```

### 查看时间

通过date可以查看当前时间

```
$ date
Sat 29 May 2021 09:06:32 PM HKT
```

可以通过格式化字符串`'+%x'`来改变打印内容，如：

```
$ date '+%Y-%m-%d'
2021-05-29
```

%后可用的字符很多，具体可以通过`date --help`查看

几个常用参数：

- `-d`通过指定的字符串格式计算时间后输出（不是输出当前时间）

计算之前的时间`n option ago`

```
$ date -d '2 days ago' '+%Y-%m-%d'
2021-05-27
```

计算之后的时间`n option`

```
$ date -d '2 months' '+%Y-%m-%d'
2021-07-29
```

option值：years年，months月，weeks周，days天，hours小时，minutes分钟，seconds秒

- `-s`设定系统时间为指定字符串


### 查看进程状态

`ps`(process status)命令

常用方法：

- `-ef`，显示所有进程信息，连同命令行，常与grep结合使用，用于根据程序查找进程

示例：

```
$ ps -ef | grep mysqld
chunar    3094 22690  0 21:39 pts/1    00:00:00 grep mysqld
systemd+ 21368 21274  0 May27 ?        00:10:24 mysqld
```
- `aux`，列出当前正在内存中的进程，显示CPU占用，内存占用以及进程状态等信息

示例：

```
$ ps aux | head -n 3
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.3 170792  6328 ?        Ss   Apr13   4:27 /lib/systemd/systemd --system --deserialize 20
root         2  0.0  0.0      0     0 ?        S    Apr13   0:02 [kthreadd]
```

各字段含义：

1.USER，进程属于的用户

2.PID，进程号

3.%CPU，CPU占用率

4.%MEM，内存占用率

5.VZS，虚拟内存占用量（K）

6.RSS，占用的固定内存量（k）

7.TTY，在哪个中断机上运行，与终端无关则显示`?`，tty1-tty6表示在本机运行，若为`pts`则为远程登陆

8.STAT，状态，主要有几种：`R`正运行或就绪，`S`睡眠状态，需要被signal唤醒，`T`停止，`Z`僵尸状态

9.START，该进程的启动时间

10.TIME，进程在CPU上运作的时间

11.COMMAND，运行程序的指令

通过aux，可以实现根据CPU或内存占用率排序进程：

- 通过CPU占用率排序

```
$ ps aux --sort=-pcpu | head -n 4
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root      6002  0.2  4.6 1013092 88860 ?       Sl   Apr27 126:03 /usr/local/qcloud/YunJing/YDEyes/YDService
root     27847  0.2  0.6 624004 13340 ?        Sl   May16  65:23 barad_agent
root      6026  0.1  1.0 633456 19548 ?        Sl   Apr27  53:58 /usr/local/qcloud/YunJing/YDEdr
```

`--sort`指定按哪一列来排序，使用p来代替%，同时按递减顺序排序需要取负数：`--sort=-pcpu`

- 通过内存占用率排序

```
$ ps aux --sort=-pmem | head -n 4
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
systemd+ 21368  0.1 21.2 1281248 406232 ?      Ssl  May27  11:18 mysqld
root      6002  0.2  4.6 1013356 89148 ?       Sl   Apr27 126:03 /usr/local/qcloud/YunJing/YDEyes/YDService
root      9916  0.1  4.4 978000 85764 ?        Ssl  May11  44:57 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```

- `-eo`指定要输出的列

示例

```
$ ps -eo user,pcpu,pmem,stat --sort=-pmem | head -n 4
USER     %CPU %MEM STAT
systemd+  0.1 21.2 Ssl
root      0.2  4.6 Sl
root      0.1  4.4 Ssl
```

注意选择多个列时中间不能有空格


### 排序

通过`sort`命令来对文本每一行排序，可以指定多种排序形式，以`testfile`为例：

```
1-22-333 4 2
3-33-444 3 12
2-11-222 2 13
4-44-111 1 3
```

默认按照每行第一个字符的字典序排序：

```
$ cat testfile | sort
1-22-333 4 2
2-11-222 2 13
3-33-444 3 12
4-44-111 1 3
```

- `-r`倒序

```
$ cat testfile | sort -r
4-44-111 1 3
3-33-444 3 12
2-11-222 2 13
1-22-333 4 2
```

- `-k`，默认以tab或空格为分隔符，指定按照第几个元素排序

```
$ cat testfile | sort -k2
4-44-111 1 3
2-11-222 2 13
3-33-444 3 12
1-22-333 4 2
```

`-k2`指定以第二列（1, 2, 3, 4那一列)排序

- `-t`指定分隔符

```
$ cat testfile | sort -t'-' -k2
2-11-222 2 13
1-22-333 4 2
3-33-444 3 12
4-44-111 1 3
```

指定'-'为分隔符，第二列变成了11, 22, 33, 44那一列

- `-n`按照数字大小排序，而不是字典序

若直接按照最后一列排序，12与13排在2和3的前面：

```
$ cat testfile | sort -k3
3-33-444 3 12
2-11-222 2 13
1-22-333 4 2
4-44-111 1 3
```

指定`-n`：

```
$ cat testfile | sort -k3 -n
1-22-333 4 2
4-44-111 1 3
3-33-444 3 12
2-11-222 2 13
```
