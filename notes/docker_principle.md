Docker采用`c/s`结构，服务端作为守护进程运行在后台接收客户端的请求

## 命名空间 Namespace

Docker借助Linux内核的命名空间特性实现了容器之间的`隔离性`

- PID命名空间，不同用户的进程通过PID命名空间隔离

- net命名空间，实现了网络隔离，Docker采用veth的方式，将容器的`虚拟网卡`与宿主机的Docker网桥`Docker0`连接在一起

- ipc命名空间，进程间交互（interprocess communication, ipc），容器的进程间交互实际上是`宿主机`上具有相同pid命名空间的进程交互

- mnt命名空间，允许不同命名空间的进程看到的`文件结构`不同（mount, 挂载）

- uts命名空间，(UNIX Time-sharing System)允许每个容器有独立的`hostname`和`domin name`

- user命名空间，允许在容器内创建容器内部的`用户和用户组`

## 控制组

控制组（cgroups）也是Linux内核的特性，用于控制对`共享资源的分配`

通过控制组可以对容器的内存、CPU和I/O资源进行`限制`和`审计`，防止某个容器占用过多资源

## 联合文件系统

联合文件系统(UnionFS)是一种`分层`的文件系统

联合文件系统让Docker实现了分层继承，基于基础镜像可以创建不同的具体镜像

而且不同的Docker容器可以`共享`一些基础文件系统层，提高了存储效率

## OCI

Open Container Initiative是一种容器规范化标准，它目前定义了两种标准：`容器运行时标准`和`容器镜像标准`

Docker也采用了OCI标准，并通过runc（一个golang编写的轻量化容器运行工具）来运行容器：

[![2zuCuV.png](https://z3.ax1x.com/2021/06/17/2zuCuV.png)](https://imgtu.com/i/2zuCuV)