## 常用方法

- 新建变量时等号旁边`不能加空格`

```
a="test"
echo $a
```

- 通过计算得到新变量时要加`两个括号`

```
a=1
b=2
c=$(($b+$a))
echo $c
```

### 判断

#### test

test的功能很强大，可以判断两个值是否相等，还可以判断文件类型等

判断数值：

- `-eq`，相等

- `-ne`，不相等

- `-gt`，大于

- `-ge`，大于等于

- `-lt`，小于

- `-le`，小于等于

示例：

```shell
$ test 1 -gt 2 && echo true || echo false
false
```

字符串：

- `=`，相等

- `!=`，不相等

- `-z`，长度为0

- `-n`，长度不为零

示例：

```shell
$ test -z "123" && echo true || echo false
false
```

文件：

- `-e filename`，文件存在

- `-r filename`，文件存在且可读

- `-w filename` ，文件存在且可写

- `-x filename`，文件存在且可执行

- `-s filename`，文件存在且不为空

- `-d filename`，存在且为文件夹

- `-f filename`，存在且为普通文件

- `-c filename`，存在且为字符型文件

- `-b filename`，存在且为块文件

示例：

```shell
$ touch testfile
$ test -f testfile && echo true || echo false
true
```

逻辑运算

- `-a`，与

- `-o`，或

- `!`，非

示例：

```shell
$ test 1 -eq 2 -o -n "123" && echo true || echo false
true
```

#### 中括号

与test类似，只是将判断语句写进了`[]`中，如

```shell
$ [ 2 -gt 1 ] && echo true || echo false
true
```

注意`[]`每一个元素之间都要加空格

#### if语句

使用形式是：

```sh
if condition; then

elif condition; then

else

fi
```

编写一个脚本，测试输入的文件名是否存在：

```sh
#!/bin/bash
read -p "input a file name to check if it's existed: " file

if test -e $file; then
	echo "true"
else
	echo "false"
fi
```

### 循环

#### while循环

句式：

```shell
while condition
do
    command
done
```

示例：

```shell
#!/bin/bash

num=0

while ((num<100))
do
	echo $num
	((num+=10))
done
```

- 双括号`(())`中可以直接进行数值运算，不用加上`$`

#### until循环

与while相反，until是一旦条件满足就退出循环，要想与上面的示例达到相同效果：

```shell
#!/bin/bash

num=0

until ((num>=100))
do
	echo $num
	((num+=10))
done
```

#### for循环

想要达到同一效果：

```shell
#!/bin/bash

for((num=0;num<100;num+=10))
do
	echo $num
done
```

for循环还可以很方便的遍历各种已知的序列，下面的脚本可以打印出输入路径中所有的文件：

```shell
#!/bin/bash

read -p 'input a directory: ' dir

files=`ls $dir`

for filename in $files
do
	echo $filename
done
```

### 脚本定时运行

通过`crontab`来定时运行命令（不只是shell脚本）

crontab命令的参数：

```
crontab –e      //修改 crontab 文件，如果文件不存在会自动创建
crontab –l      //显示 crontab 文件
crontab -r      //删除 crontab 文件
crontab -ir     //删除 crontab 文件前提醒用户
```

crontab定时任务编写的基本格式：

```
*　　   *　　    *　　    *　　     *　　command
分     时　     日　     月　      周　  命令
0-59   0-23    1-31     1-12     0-6
```

每一列除了填写数字，还可以使用一些符号：

```
*        代表任何时间，比如第一个 * 就代表一小时中的每分钟都执行
,        代表不连续的时间，比如 0 8,12,16 * * * 代表每天8，12，16点0分执行
-        代表连续的时间范围，比如0 5 * * 1-6 代表在周一到周六凌晨5点0分执行
*/n      代表每个多久执行一次，比如*/10 * * * *代表每隔10分钟执行一次
```

假设编写好一个`test.sh`脚本，要每十分钟运行一次：

```
$ crontab -e
```

输入内容：

```
*/10 * * * * /bin/bash /tmp/test.sh
```

保存退出即可

## 例题

- 当服务器负载超过5时（低于5时，什么也不做，脚本退出）打印服务器的内存，磁盘I/O使用情况，并列出占用CPU资源较大的1-10位

```sh
#!/bin/bash

# 通过uptime查看cpu负载，在awk中进行判断
load=`uptime | awk '$12>=5{print $12}'`

# 如果load小于5，就直接退出
if [ -z "$load" ]; then
	echo "load is low"
	exit 0
else
	echo "the load is: $load"
	# 通过vmstat查看cpu，内存和IO使用
	echo "the cpu and mem: "
	echo `vmstat | sed -n '2p'`
	echo `vmstat | sed -n '3p'`
	echo "10 most processes: "
	# 通过ps aux查看各个进程
	echo `ps aux --sort=-pcpu | head -n 11 | awk 'NR>1{print $2}'`
fi
```