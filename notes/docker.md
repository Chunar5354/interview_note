## 安装

[官方网站](https://docs.docker.com/engine/install/)给的非常详细，可以直接根据自己的系统版本进行安装

## 如何运行一个镜像

以mysql为例，首先搜索一下可以安装的镜像

```
$ sudo docker search mysql
```

会出现类似下面的结果

```
NAME                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
mysql                             MySQL is a widely used, open-source relation…   10665     [OK]
mariadb                           MariaDB Server is a high performing open sou…   3997      [OK]
mysql/mysql-server                Optimized MySQL Server Docker images. Create…   779                  [OK]
percona                           Percona Server is a fork of the MySQL relati…   528       [OK]
centos/mysql-57-centos7           MySQL 5.7 SQL database server                   87
```

其中OFFICIAL字段下带有[OK]标识的说明是官方维护，STARS表示受欢迎程度，这里选择第一个镜像进行安装：

```
$ sudo socker pull mysql
```

然后查看一下已经安装的镜像

```
$ sudo docker images
```

此时只是安装了镜像，并没有运行起来，输入下面的命令运行镜像：

```
$ sudo docker run --name mysql -p 12000:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql
```

其中`--name`是为容器指定一个名称，`-p`是提供一个本地主机到容器的端口映射，比如上面就是将本地的12000端口映射到了容器的3306端口，`-e`是设置环境变量，这里是为mysql设置默认的root密码，`-d`是让容器以守护进程的方式在后台运行

运行起来之后，用下面的代码查看容器信息：

```
$ sudo docker ps -a
// 或者
$ sudo docker container ls -a
```

会看到下面的信息：

```
CONTAINER ID   IMAGE         COMMAND                  CREATED             STATUS                         PORTS                                NAMES
93eaaf1bce47   mysql         "docker-entrypoint.s…"   34 minutes ago      Up 34 minutes                  33060/tcp, 0.0.0.0:12000->3306/tcp   mysql
```

STATUS字段中带有`Up`，表示当前容器正在运行

- 一些关于镜像和容器的操作：

```
$ sudo docker rmi 镜像ID    // 删除镜像
$ sudo docker stop 容器ID   // 停止运行容器
$ sudo docker rm 容器ID     // 删除容器，只有停止的容器才能被删除
```

进入容器的终端：

```
sudo docker exec -it 容器ID(或容器NAME) bash
```

`-i`参数会打开标准输入，`-t`参数会为容器分配伪终端，带上这两个参数就可以在命令行像控制本地计算机一样控制容器

对于mysql容器，为了测试，开启一下远程登录权限:

```
root@aae4af45885a:/# mysql -u root -p123456
mysql> ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
```

然后`exit`返回本地终端

想要远程连接容器中的mysql，需要知道容器的IP地址，通过下面的命令:

```
$ sudo docker inspect 容器ID | grep IPAddress
```

在本地远程连接容器中的mysql：

```
$ mysql -h 容器IP -P 3306 -u root -p123456
```

## 创建镜像

### Dockerfile

常用命令，[官方说明](https://docs.docker.com/engine/reference/builder/#from)

- FROM，表名镜像来自哪个基础镜像

- LABEL，指定标签

- RUN，执行的shell命令

- ADD，拷贝文件并解压

- COPY，拷贝文件

- EXPOSE，暴露端口

- ENV，设置环境变量

- CMD，启动容器后要运行的程序

- ENTRYPOINT，与CMD类似，但不会被启动容器时的附加命令覆盖

- WORKDIR，设置自动跳转到某个路径

### 利用Dockerfile部署django项目

首先要整理好文件目录，为了便于管理，通常将项目文件（一会要添加进镜像）和Dockerfile放在一起

```
some_path/
    Dockerfile
    my_project/
    start.sh
    blog.ini
    pip.conf
```

其中，`start.sh`是容器创建后要运行的命令：

```
#!/bin/bash

python my_project/manage.py makemigrations&&
python my_project/manage.py migrate&&
uwsgi /home/my_project/blog.ini
```

`blog.ini`是代理django项目的uwsgi文件:

```
[uwsgi]
socket = 0.0.0.0:12000
chdir = /home/my_project/my_project/
module = my_project.wsgi:application
```

`pip.conf`用于给镜像的pip换源加速:

```
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com

```

最后是Dockerfile：

```
# 基础镜像为Python最新版
FROM python

# 指定作者
LABEL maintainer="Chunar"

# pip换源
COPY pip.conf /root/.pip/pip.conf

# 创建工作文件夹
RUN mkdir -p /home/my_project

# 设置容器工作目录
WORKDIR /home/my_project

# 拷贝本地文件到容器
ADD . /home/my_project

# 自动安装
RUN pip install -r my_project/requirements.txt
RUN pip install uwsgi mysqlclient

# 赋予脚本执行权限
RUN chmod +x ./start.sh

CMD ["/home/my_blog/start.sh", "run"]
```

通过Dockerfile指定了镜像要做的事情：

- 1.首先安装Python最新版镜像作为基础

- 2.为pip换源

- 3.创建工作文件夹并进入

- 4.将本地项目以及配置文件拷贝到容器工作目录

- 5.安装依赖

- 6.执行脚本

通过上面的Dockerfile创建一个镜像：

```
sudo docker build -f Dockerfile -t my_project /some_path/
```

`-f`指定通过哪个文件来创建镜像，`-t`指定镜像名称，后面的路径指定本地目录，Dockerfile中的`ADD`都是相对于/some_path/的相对路径

运行镜像：

```
sudo docker run -it --name my_project -p 12000:12000 -d my_project
```

由于容器的IP地址对外部可见，所以需要绑定到本地计算机的端口，此时在浏览器输入

```
http://localhost:12000
```

就可以看到django项目的界面

## 迁移镜像

镜像的迁移有两种方式，通过本地save成tar包或上传到docker hub

### 本地save

首先将本地的镜像打包成一个tar包：

```
$ sudo docker save -o /your_path/your_image.tar your_image
```

`-o`参数用于指定tar包的存储路径

然后将这个tar包拷贝到目标机器上，通过load导出成镜像：

```
$ sudo docker load -i /your_path/your_image.tar
```

`-i`参数用于指定tar包的路径

此时镜像就已经导入到目标主机中了

### 使用docker hub

除了打包成本地文件的形式，还可以将自己的镜像上传到公共仓库，这样别人也能够使用自己的镜像

首先需要创建一个docker hub账号，[地址](https://hub.docker.com/)

然后在本地客户端登录

```
$ sudo docker login
```

要上传自己的镜像，首先需要为本地镜像打上`标签`

```
$ sudo docker tag local-image:tagname your_id/repo_name:tagname
```

其中tagname是自己指定的版本，如果没有则默认是latest

然后上传到公共仓库：

```
$ sudo docker push your_id/repo_name:tagname
```

此时自己的镜像就已经被上传到docker的公共仓库中，可以像其它的镜像一样search和pull


### 私有仓库

#### 搭建私有仓库

搭建私有仓库需要借助官方的registry镜像来实现

```
$ sudo docker pull registry
```

然后编辑配置文件`/etc/docker/daemon.json`（如果没有就新建一个），写入以下内容：

```json
{
    "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"],
    "insecure-registries": ["192.168.1.10:12020"]
}
```

第一项是指定镜像加速元，第二项是`本机IP`+将要绑定到容器的`本机端口`

然后重启

```
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

创建registry容器

```
$ sudo docker run -di --name registry -p 12020:5000 -v /youe_path:/var/lib/registry registry
```

注意要将之前配置的本地端口映射到registry容器的`5000`端口

此时在浏览器输入`http://your_ip:12020/v2/_catalog`就可以看见`{"repositories":[]}`字样，说明私有仓库创建成功

#### 上传镜像到私有仓库

与上传到公共仓库类似，不过要将your_id部分改成上面的`your_ip:12020`(自己的端口号)

```
$ sudo docker tag local-image:tagname your_ip:12020/repo_name:tagname
$ sudo docker push your_ip:12020/repo_name:tagname
```

再次打开`http://your_ip:12020/v2/_catalog`，发现registories字段中多了一个repo_name，说明上传成功

#### 从私有仓库下载镜像

如果在其他的计算机上想要下载私有仓库的镜像，那么必须在这台计算机的`/etc/docker/daemon.json`中将`insecure-registries`这一项与私有仓库配置成相同

然后可以正常拉取镜像

```
$ sudo docker pull your_ip:12020/repo_name:tagname
```