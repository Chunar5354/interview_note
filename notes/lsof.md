lsof（list open files）用于查看进程打开的文件，也可以用来查看网络端口等信息（因为socket也是文件）

## 常用方法

- `lsof <filename>`查看哪些进程打开了这个文件，如

```
lsof /bin/bash
```

- `+d`，查看哪些进程打开了文件夹以及文件夹下的文件（只查询`一层`，不向下递归），如

```
lsof +d /tmp
```

- `+D`，查看哪些进程打开了文件夹以及所有子文件夹下的文件（会一直递归到所有深度），如

```
lsof +D /tmp
```

- `-p`，查看某个进程打开的所有文件，如

```
lsof -p $$
```

查看当前shell脚本打开的文件

- `-c`，查看指定名称的程序打开的文件，如

```
lsof -c python
```

-c选项支持正则表达式

- `-i`，查看网络相关的文件

```
lsof -i          // 查看所有IPv4和IPv6网络打开的文件
lsof -i 4        // 查看IPv4打开的文件
lsof -i 6        // 查看IPv6打开的文件
lsof -i:80       // 查看80端口相关的文件
lsof -i:1-1024   // 查看1到1024端口相关的文件
```

## 输出详解

以`lsof -p $$`为例：

```
(base) chunar@VM-4-10-debian:~$ sudo lsof -p $$
COMMAND  PID   USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
bash    6469 chunar  cwd    DIR  254,1     4096 655361 /home/chunar
bash    6469 chunar  rtd    DIR  254,1     4096      2 /
bash    6469 chunar  txt    REG  254,1  1168776 263824 /usr/bin/bash
bash    6469 chunar  mem    REG  254,1   146968 262834 /usr/lib/x86_64-linux-gnu/libpthread-2.28.so
bash    6469 chunar  mem    REG  254,1    35808 262836 /usr/lib/x86_64-linux-gnu/librt-2.28.so
bash    6469 chunar  mem    REG  254,1   282752 266922 /usr/lib/x86_64-linux-gnu/libnss_systemd.so.2
bash    6469 chunar  mem    REG  254,1    55792 262829 /usr/lib/x86_64-linux-gnu/libnss_files-2.28.so
bash    6469 chunar  mem    REG  254,1    26402 265269 /usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache
bash    6469 chunar  mem    REG  254,1  3036368 280781 /usr/lib/locale/locale-archive
bash    6469 chunar  mem    REG  254,1  1824496 262816 /usr/lib/x86_64-linux-gnu/libc-2.28.so
bash    6469 chunar  mem    REG  254,1    14592 262820 /usr/lib/x86_64-linux-gnu/libdl-2.28.so
bash    6469 chunar  mem    REG  254,1   183528 265621 /usr/lib/x86_64-linux-gnu/libtinfo.so.6.1
bash    6469 chunar  mem    REG  254,1   165632 262185 /usr/lib/x86_64-linux-gnu/ld-2.28.so
bash    6469 chunar    0u   CHR  136,0      0t0      3 /dev/pts/0
bash    6469 chunar    1u   CHR  136,0      0t0      3 /dev/pts/0
bash    6469 chunar    2u   CHR  136,0      0t0      3 /dev/pts/0
bash    6469 chunar  255u   CHR  136,0      0t0      3 /dev/pts/0
```

从左到右各个字段分别表示：

- COMMAND，程序名称

- PID，进程号

- USER，进程所属的用户

- FD，进程通过哪种文件描述符来识别该文件，有以下几种类型：

    - cwd，当前工作目录
    - rtd，根目录
    - txt，运行该程序的可执行文件
    - mem，内存映射文件
    - 0u，1u等数字，表示标准输入输出文件，`u`表示处于读写模式，`r`表示只读，`w`表示只写，如果有`W`表示持有写锁

- TYPE，文件类型，DIR表示文件夹，REG表示普通文件，CHR表示字符，BLK表示块设备

- DIVICE，设备编号

- SIZE/OFF，文件大小

- NODE，索引节点（文件在磁盘上的标识）

- NAME，文件绝对路径
