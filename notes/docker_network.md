前置：关于Docker的基础应用请看[这里](https://chunar5354.github.io/2021/03/29/docker-using.html)

Docker的网络模式

## 网络模式简介

Docker主要有四种网络模式：bridge，host，none和container

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
