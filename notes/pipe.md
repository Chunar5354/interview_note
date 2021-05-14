Linux中`|`为管道命令，它可以连接多个命令，将前面命令的输出作为后面命令的输入，从而将数据进行多级处理显示出来

在管道中间传递的信息都是`标准输入输出`，所以在`|`前面的命令必须能够输出到标准输出，后面的命令必须能够接收来自标准输入的数据

## 常用管道命令

### cut

cut用于以`行`为单位`截取`文本

cut有两种常用的命令形式：

- 1.`cut -d'delimiter' -f fields`

将文本以`delimiter`为分隔符分割，并输出第`fields`个元素

如

```shell
(base) chunar@VM-4-10-debian:~$ echo $PATH
/home/chunar/anaconda3/bin:/home/chunar/anaconda3/condabin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/usr/local/go/bin
(base) chunar@VM-4-10-debian:~$ echo $PATH | cut -d':' -f 3
/usr/local/bin
```

上面第二条命令表示将结果以':'分割，并取第三个输出，结果为'/usr/local/bin'

对于`-f`后面的参数，可以有不同形式，`-n`表示输出第1个到第n个结果，`n-`表示输出从第n个到最后一个结果，`n-m`表示第n个到第m个（全是闭区间），`n,m`表示输出第n个和第m个，如

```shell
(base) chunar@VM-4-10-debian:~$ echo $PATH | cut -d':' -f -3
/home/chunar/anaconda3/bin:/home/chunar/anaconda3/condabin:/usr/local/bin
(base) chunar@VM-4-10-debian:~$ echo $PATH | cut -d':' -f 3-
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/usr/local/go/bin
(base) chunar@VM-4-10-debian:~$ echo $PATH | cut -d':' -f 3-5
/usr/local/bin:/usr/bin:/bin
(base) chunar@VM-4-10-debian:~$ echo $PATH | cut -d':' -f 3,5
/usr/local/bin:/bin
```

- 2.`cut -c characters`

表示以characters为单位取出`每一行`的固定`字符区间`

```shell
(base) chunar@VM-4-10-debian:~$ ls / -l | head -4
total 64
lrwxrwxrwx   1 root root     7 Jan 10  2020 bin -> usr/bin
drwxr-xr-x   3 root root  4096 Apr 30 14:00 boot
drwxr-xr-x   2 root root  4096 Mar  8 21:14 data
(base) chunar@VM-4-10-debian:~$ ls / -l | head -4 | cut -c 14-

1 root root     7 Jan 10  2020 bin -> usr/bin
3 root root  4096 Apr 30 14:00 boot
2 root root  4096 Mar  8 21:14 data
(base) chunar@VM-4-10-debian:~$ ls / -l | head -4 | cut -c 14-20

1 root 
3 root 
2 root
```

### grep

grep全称是`Global Regular Expression Print`，通过正则表达式来搜索文本，并打印`匹配的行`

如果带上`-v`参数则打印`除匹配的行之外`的所有行，如

```shell
(base) chunar@VM-4-10-debian:~$ ls / -l | head -4
total 64
lrwxrwxrwx   1 root root     7 Jan 10  2020 bin -> usr/bin
drwxr-xr-x   3 root root  4096 Apr 30 14:00 boot
drwxr-xr-x   2 root root  4096 Mar  8 21:14 data
(base) chunar@VM-4-10-debian:~$ ls / -l | head -4 | grep 'root'
lrwxrwxrwx   1 root root     7 Jan 10  2020 bin -> usr/bin
drwxr-xr-x   3 root root  4096 Apr 30 14:00 boot
drwxr-xr-x   2 root root  4096 Mar  8 21:14 data
(base) chunar@VM-4-10-debian:~$ ls / -l | head -4 | grep 'root' -v
total 64
```

### sort

将结果的每一`行`按照`字典序`排序

```shell
(base) chunar@VM-4-10-debian:~$ cat testfile
abc:123:def
bcd:234:cdef00
cde:123:ef00
abc:456:fgh00
bcd:123:def00
(base) chunar@VM-4-10-debian:~$ cat testfile | sort
abc:123:def
abc:456:fgh00
bcd:123:def00
bcd:234:cdef00
cde:123:ef00
```

sort有一个常用的用法：

`sort -t'c' -k m`，表示将文本按照字符c来分割，并按照结果中的`第m个元素`来排序

```shell
(base) chunar@VM-4-10-debian:~$ cat testfile | sort -t':' -k 2
abc:123:def
bcd:123:def00
cde:123:ef00
bcd:234:cdef00
abc:456:fgh00
```

### wc

`wc`命令可以统计一段文本的行数（列数）、单词数以及字节数

如果只输入`wc`，默认是统计标准输入输出

```
(base) chunar@VM-4-10-debian:~/docker-images-motor$ wc
aa
dd
      2       2       6
```

从左到右分别表示2行，2个单词以及6字节

wc可以带上参数，`-l`表示只输出行数，`-w`只输出字数，`-c`只输出字节数

使用wc可以统计命令的返回结果数，如

```
$ ls | wc -l  // 当前目录下有多少个文件
```

也可以对文件进行统计，如

```
$ wc test.txt
```
