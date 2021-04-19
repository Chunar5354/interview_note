TCP连接中close与shutdown的区别

主要有两点：

- 1.close的关闭与当前socket的`引用次数`有关，即如果有其他进程也使用了当前的socket，在当前进程中close的socket并没有被删除，其它的进程依然可以使用，只有当一个socket的引用次数为0时被close的socket才真正被关闭。而shutdown与引用次数无关，在一个进程中shutdown的socket就被删除了，其它进程也`不能再使用`

- 2.shutdown可以`只关闭某一个方向`，使用shutdown时可以携带一个参数，0表示不能再读，1不能再写，2不能读和写