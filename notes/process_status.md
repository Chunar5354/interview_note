在Linux中使用top或ps命令可以查看进程的状态，各种输出表示的含义如下：

- R，Running或Runnable，正在运行或就绪状态

- D，Disk Sleep，不可中断睡眠态，一般表示进程在与`硬件`交互，并且交互过程不能被其它进程或中断打断

- Z，Zombie，僵尸进程，进程已经结束，但它的资源没有被父进程回收

- S，Interruptible Sleep，可中断睡眠状态，表示进程在等待某个事件而被挂起

- I，Idle，空闲状态，用在不可中断睡眠的内核线程上，与D区分，I状态的进程没有带负载

- T，Stopped或Traced，暂停或跟踪状态，进程接收SIGSTOP信号变成暂停状态，接收SIGCONT信号恢复运行

- X，Exit或Dead，退出状态，进程即将被销毁
