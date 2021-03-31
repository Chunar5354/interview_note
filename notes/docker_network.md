Docker的网络模式

## 网络模式简介

Docker主要有四种网络模式：bridge，host，none和container

通过下面的命令来查看当前有哪些网络：

```
$ sudo docker network ls
```

在创建容器中通过`--net`参数指定网络模式

### bridge

bridgr是默认的网络模式，会首先创建一个虚拟网络适配器`docker0`，用作所有容器的网关gateway

可以使用`ip a`命令查看系统中的网络适配器，通常docker0的IP地址是`172.17.0.1`，所配置的子网是`172.17.0.1/16`

在容器一端，docker会生成一对虚拟网卡`veth pair`，将veth pair的一端放在容器中（eth0，可以在容器中通过`ip a`查看），另一端在主机中（名称为`vethxxxx`，有几个容器在运行，主机中就会有几个对应的vethxxxx）

同时每个容器会被`按顺序`自动配置一个IP地址

[![cC26II.png](https://z3.ax1x.com/2021/03/29/cC26II.png)](https://imgtu.com/i/cC26II)

### host

host模式中，容器的IP地址与端口`直接绑定到宿主机`，不需要进行映射

### none

容器有独立的网络命名空间，但没有任何网络设置，需要用户自行配置

### container

新创建的容器不会被配置自己的IP，而是和另一个指定的容器`共享`IP和端口范围

创建方法：

```
$ sudo docker run --name c2 --net container:c1 -it your_image
```

此时c2容器的网络与c1相同

如果将c1停止，则c2就没有IP地址了，只有一个`lo`本地网络

### 自定义网络

用户可以根据上面的几种网络模式进行自定义网络

自定义网络的一个重要用途：实现容器间`通过容器名通信`而不是IP地址进行通信（因为IP地址每次创建时可能会改变）

在Docker内置了一个`DNS server`，提供IP地址到容器名的解析，但是只有自定义网络才能使用

创建自定义网络：

```
$ sudo docker network create -d bridge your_network
```

`-d`参数是指定基于哪种网络模式，默认是bridge

然后基于自定义网络创建两个容器：

```
$ sudo docker run --name c1 --net my_network -it my_image
$ sudo docker run --name c2 --net my_network -it my_image
```

此时进入c1输入`ping c2`就可以ping通

注意不同network下创建的容器即使`ping ip`也ping不通
