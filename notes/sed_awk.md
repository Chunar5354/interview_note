## sed

sed分析标准输入，将数据处理后输出到标准输出

它的强大在于可以直接将文本进行处理，如新增、删除、替换等

通用形式是：

```
$ sed -option 'operation'
```

以下以testfile作为测试文本对参数进行说明，testfile原本内容如下：

```
drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
drwxr-xr-x 4 chunar chunar 4096 May 16 16:54
drwxr-xr-x 8 chunar chunar 4096 Apr 24 21:04
drwxr-xr-x 4 chunar chunar 4096 May 27 21:44
```

常用option说明：

- `-n`表示安静模式，只会打印出被sed处理的那些行

```
$ cat testfile | sed '1i 123'  // 在第一行前面插入123
123
drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
drwxr-xr-x 4 chunar chunar 4096 May 16 16:54
drwxr-xr-x 8 chunar chunar 4096 Apr 24 21:04
drwxr-xr-x 4 chunar chunar 4096 May 27 21:44
```

如果带上-n：

```
$ cat testfile | sed -n '1i 123'
123
```

- `-f`表示通过指定的`脚本文件`来修改文本

- `-i`表示直接将修改保存到原文件，而不是打印到标准输入

- `-r` 表示使用扩展的正则表达式

常用operation说明：

全部的operation必须放在`引号`中

- `n1,[n2]`，表示操作要应用到的行数，如果没有n2，就直接对n1行进行操作，否则对n1到n2行进行操作

```
$ cat -n testfile | sed '2d'     // 删除第2行
     1	drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
     3	drwxr-xr-x 8 chunar chunar 4096 Apr 24 21:04
     4	drwxr-xr-x 4 chunar chunar 4096 May 27 21:44

$ cat -n testfile | sed '2,4d'   // 删除第2到4行
     1	drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
```

- `a`，新增内容，后面带空格加要新增的内容，如果不指定行号就在`每一行下方`新增

```
$ cat -n testfile | sed 'a 123'      // 在每一行后增加123
     1	drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
123
     2	drwxr-xr-x 4 chunar chunar 4096 May 16 16:54
123
     3	drwxr-xr-x 8 chunar chunar 4096 Apr 24 21:04
123
     4	drwxr-xr-x 4 chunar chunar 4096 May 27 21:44
123

$ cat -n testfile | sed '1,3a 123'      // 在1-3行后增加123
     1	drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
123
     2	drwxr-xr-x 4 chunar chunar 4096 May 16 16:54
123
     3	drwxr-xr-x 8 chunar chunar 4096 Apr 24 21:04
123
     4	drwxr-xr-x 4 chunar chunar 4096 May 27 21:44
```

- `c`，取代，空格带内容，这些内容取代指定的n1到n2

```
$ cat -n testfile | sed 'c 123'  // 每一行都变成123
123
123
123
123

$ cat -n testfile | sed '2,4c 123'    // 2到4行变成123
     1	drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
123
```

- `d`，删除

- `i`，插入，空格带内容，如果不指定行号就在`每一行上方`插入

```
$ cat -n testfile | sed 'i 123'   // 在每一行上方增加123
123
     1	drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
123
     2	drwxr-xr-x 4 chunar chunar 4096 May 16 16:54
123
     3	drwxr-xr-x 8 chunar chunar 4096 Apr 24 21:04
123
     4	drwxr-xr-x 4 chunar chunar 4096 May 27 21:44
```

- `p`，打印，打印某个选择的内容，通常与-n搭配使用

```
$ cat -n testfile | sed '2p'      // 第二行会重复打印
     1	drwxr-xr-x 4 chunar chunar 4096 Mar 26 19:24
     2	drwxr-xr-x 4 chunar chunar 4096 May 16 16:54
     2	drwxr-xr-x 4 chunar chunar 4096 May 16 16:54
     3	drwxr-xr-x 8 chunar chunar 4096 Apr 24 21:04
     4	drwxr-xr-x 4 chunar chunar 4096 May 27 21:44

$ cat -n testfile | sed -n '2p'   // 只查看第二行
     2	drwxr-xr-x 4 chunar chunar 4096 May 16 16:54
```

- `s`，取代，通过正则表达式`s/ogirinal/new/g`的语法来取代指定内容

```
$ cat -n testfile | sed 's/chunar/root/g'      // 将所有的'chunar'替换为'root'（g表示全部）
     1	drwxr-xr-x 4 root root 4096 Mar 26 19:24
     2	drwxr-xr-x 4 root root 4096 May 16 16:54
     3	drwxr-xr-x 8 root root 4096 Apr 24 21:04
     4	drwxr-xr-x 4 root root 4096 May 27 21:44

$ cat -n testfile | sed 's/chunar/root/'       // 将每一行的第一个'chunar'替换为'root'
     1	drwxr-xr-x 4 root chunar 4096 Mar 26 19:24
     2	drwxr-xr-x 4 root chunar 4096 May 16 16:54
     3	drwxr-xr-x 8 root chunar 4096 Apr 24 21:04
     4	drwxr-xr-x 4 root chunar 4096 May 27 21:44
```

## awk

相对于sed对一整个行的处理，awk更适合对每一行`分字段`进行处理

awk命令中，operation也是要包含在`''`中，具体实现的操作要包含在`{}`中，如(仍然以testfile为例):

```
$ awk '$2 < 5 {print $2"-"$3}' testfile
4-chunar
4-chunar
4-chunar
```

awk会默认以`空格`或`tab`作为分隔符，将每一行的内容分割，并用`$n`表示第n个元素

在上面的命令中，单引号内不在{}中的部分表示`条件语句`，`$2 < 5`即第二个元素小于5，后面的`{print $2"-"$3}`表示打印第二个和第三个元素，并在二者中间插入"-"

awk有很多预设好的内置变量，具体可以查看[这里](https://www.runoob.com/linux/linux-comm-awk.html)，本文列出一些比较常用的：

- `NF`，每一行则字段总数

- `NR`，行号

- `FS`，分隔符

示例：

```
$ awk 'BEGIN {FS="-"} {print NR":"NF}' testfile
3:xr
3:xr
3:xr
3:xr
```

上面的命令中，通过`{FS="-"}`指定了分隔符为"-"，`BEGIN`的作用是从`第一行`开始，如果不加BEGIN，第一行的分隔符还是默认字符

然后以`行号:每行字段数`的格式打印文本

在awk中也可以自己`新建变量`，示例：

```
$ awk 'NR==2{sum=$2+$7
> printf"%8s%8s%8s\n",$2,$7,sum}' testfile
       4      16      20
```

通过`NR==2`指定第二行，新建变量sum，值为第2个与第7个变量之和，并通过printf格式化打印（自建变量不需要加$）

在同一个{}内执行多个动作时，每个动作以`回车`或`;`分割，所以下面的命令与上面的命令相同

```
$ awk 'NR==2{sum=$2+$7;printf"%8s%8s%8s\n",$2,$7,sum}' testfile
```

### 浮点数运算

bash shell本身不支持浮点数运算，使用awk可以完成简单的浮点数运算和判断

```shell
#!/bin/bash

a=1.1

read -p "input b: " b

ans=`echo | awk "$b > 5 {print($a/$b)}"`

echo $ans
```

上面的脚本实现输入一个任意数字b，当大于5时，输出1.1/b的结果

有两点注意：

- 1.awk单独使用时会等待标准输入，所以要获取awk的结果时通常使用`echo | awk ...`的形式

- 2.为了在表达式中使用变量，表达式需要用`双引号`