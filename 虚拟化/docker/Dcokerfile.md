Dockerfile是docker构建image的文件，docker通过docker build 指定Dockerfile并根据里面的内容来构建一个docker镜像。

构建由 Docker 守护程序运行，构建过程做的第一件事是将整个上下文（递归地）发送到守护进程。构建的上下文是指定位置PATH或URL. PATH是本地文件系统的目录。URL是一个 Git 存储库位置。默认Dockerfile文件在上下文跟中

```
docker build [选项] [path/url]
  --tag,-t    镜像名            指定镜像的存储库和标签，可以用多个 -t 来指定多个存储库标签
  --file,-f   Dockerfile        Dockerfile的名称，默认PATH/Dockerfile
  --no-cache
```

docker build path/url 时，会将此路径下所有文件加入守护进程中，如果不需要，可以使用 .dockerignore文件来忽略

.dockerignore 和 .gitignore用法一致


### 镜像

docker镜像使用分层技术，通过 union filesystem 将多个文件系统叠加在一起，组成一个镜像
每一个Dockerfile关键字即为一层文件系统，加上父镜像，总不能超过128层

* linux空间
  * 内核空间(bootfs)
  * 用户空间(rootfs)

bootfs主要包含bootloader和 kernel， bootloader主要是引导加载 kernel，当 kernel被加载到内存之后 boots就被卸载掉了。 rootfs包含的就是典型linux系统中的/dev，/proc，/bin，/etc等标准目录

对于docker而言，只用到rootfs

* rootfs
  * 传统模式下：启动时，内核将rootfs挂载为只读，完成自检后改为读写
  * docker中：rootfs由内核挂载为只读，通过 UFS 技术挂载一个读写层，即容器层，所以容器状态的改变不会改变镜像






### Dockerfile语法

**指令不区分大小写。但是，惯例是将它们大写以更轻松地将它们与参数区分开**

```yml
FROM          #从哪个镜像开始构建
ENV           #设置环境变量
WORKDIR       #切换工作目录
ADD           #添加文件目录到镜像内
COPY          #添加文件目录到镜像内
RUN           #
EXPOSE        #开放端口，例如 EXPOSE 80/udp 即开放容器 80的udp端口，默认为tcp，不写即tcp
VOLUME        #
CMD           #
ENTRYPOINT    #入口点，写容器运行命令
 
```


Dockerfile示例
```yaml

ADD abc.tar.gz /tmp
ENV JAVA_HOME=/opt/jre...
```


### ADD 和 COPY

都是把文件或者目录复制进镜像

* ADD
  * 如果目标路径不存在，则创建
  * 如果拷贝文件是压缩文件，如.tar等，会自动解压，并删除原压缩文件，例 a.txt 打包成的 a.tar ADD到镜像中，镜像中只存在 a.txt
  * 可以添加远程URL文件，但是建议用 RUN 命令添加远程URL文件
* COPY
  * 如果目录路径不存在，不会创建
  * 拷贝压缩文件时，不会自动解压、
  * 只能添加打包镜像时候的宿主机的文件


### CMD 和 ENTRYPOINT

容器运行模式，CMD 和 ENTRYPOINT 都支持exec和shell模式,官方推荐exec模式
```
exec
  CMD ["top","-c"]
  ENTRYPOINT ["top","-c"]

shell
  CMD top -c
  ENTRYPOINT top -c
```
* exec
  * 容器中的任务进程的PID=1
  * 不会通过 shell 执行相关的命令，例如宿主机的环境变量 $HOME 等就取不到
  * 可以把CMD中的变量传递给ENTRYPOINT中，可以在run的时候传递参数给执行命令
* shell
  * 容器中的PID为1的进程为 /bin/sh -c "task command"(docker stop等命令都是操作PID=1的进程)
  * 可以获取宿主机的环境变量，例如 ENTRYPOINT echo $HOME 就能输出执行用户的家目录
  * 不能传参数给执行命令，不论是CMD传递给ENTRYPOINT 还是docker run 的时候后面添加的参数


#### CMD 和 ENTRYPOINT 区别
* CMD
  * 默认执行体，如果不存在entrypoint，也没有在docker run时指定执行命令，则容器启动时执行CMD中命令
  * 一个文件存在一个CMD，存在多个不报错，但只有最后一个生效
* ENTRYPOINT
  * 官方推荐容器启动执行体
  * 可以存在多个不报错，但只有最后一个生效，且会覆盖CMD

#### CMD 和 ENTRYPOINT 作用

* CMD
  * CMD ["param1","param2"] 为ENTRYPOINT传递默认参数，且ENTRYPOINT也必须是exec模式
  * CMD ["executable","param1","param2"] 默认启动执行体，exec模式
  * CMD command param1 param2 默认启动执行体，shell模式
* ENTRYPOINT
  * ENTRYPOINT ["executable","param1","param2"] exec模式
  * ENTRYPOINT command param1 param2 shell模式

命令行参数可以覆盖CMD执行体，但是不能给CMD传递参数，不论exec模式还是shell模式都可以覆盖
例：此Dockerfile打成的 a 镜像，docker run时 使用 ps aux 替换执行体，则容器执行的命令为 ps aux
```
FROM alpine
CMD ["top"]

docker build a ps aux
```
* 当CMD为exec模式，ENTRYPOINT 为exec模式，命令行参数会覆盖CMD参数为ENTRYPOINT提供参数。
* 当ENTRYPOINT为shell模式时，无论CMD还是命令行都不能给ENTRYPOINT传递参数
* ENTRYPOINT也可以在docker run时指定替换，需要显示指定 --entrypoint
* Dockerfile中至少要有CMD或者ENTRYPOINT中的一个

#### CMD 和 ENTRYPOINT 同时存在

* 如果 ENTRYPOINT 使用了 shell 模式，CMD 指令会被忽略。
* 如果 ENTRYPOINT 使用了 exec 模式，CMD 指定的内容被追加为 ENTRYPOINT 指定命令的参数。
* 如果 ENTRYPOINT 使用了 exec 模式，CMD 也应该使用 exec 模式。



### 其他

-e xxx=123 容器内 $xxx

添加环境变量
```
ENV JAVA_HOME=/opt/jre1.8.0_311
ENV PATH=$PATH:$JAVA_HOME/bin
```
