Linux常用命令

- 查看cpu信息

```
$ cat /proc/cpuinfo
```

- 查看内存信息

```
$ cat /proc/meminfo
```

或

```
$ free
```

free可以带参数，`-k`, `-m`, `-g`分别表示以KB，MB和GB为单位来表示内存大小

- 查看系统版本

```
$ uname -a
或
$ lsb_release
```

- 查看网络适配器

```
$ ip a
```