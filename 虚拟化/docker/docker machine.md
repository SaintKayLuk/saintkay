# docker machine

Docker Machine是一种工具，可让您在虚拟主机上安装Docker Engine，并使用docker-machine命令管理主机。您可以使用Machine在本地Mac或Windows盒，公司网络，数据中心或Azure，AWS或DigitalOcean等云提供商上创建Docker主机。


# 安装 docker machine

**前提: 安装docker**

* macOS 

~~~
curl -L https://github.com/docker/machine/releases/download/v0.16.0/docker-machine-`uname -s`-`uname -m` -o /usr/local/bin/docker-machine && chmod +x /usr/local/bin/docker-machine
~~~

* Linux
方式一：
~~~
curl -L https://github.com/docker/machine/releases/download/v0.16.0/docker-machine-`uname -s`-`uname -m` -o /usr/local/bin/docker-machine && chmod +x /usr/local/bin/docker-machine
~~~
方式二：
直接去github下载文件放到/usr/local/bin/下，[下载地址](https://github.com/docker/machine/releases)
修改文件名为docker-machine
chmod +x /usr/local/bin/docker-machine

因为curl下载的超级慢，还有可能下载一半的时候网络超时断掉，我用的就是第二种方式

* windows
如果您使用Git BASH运行Windows

~~~
mkdir -p "$HOME/bin" &&
curl -L $https://github.com/docker/machine/releases/download/v0.16.0/docker-machine-Windows-x86_64.exe > "$HOME/bin/docker-machine.exe" &&
chmod +x "$HOME/bin/docker-machine.exe"
~~~


# docker machine 安装docker机器

在宿主机内安装多个docker虚拟机

~~~
docker-machine create --driver virtualbox docker1
docker-machine create docker1
~~~
--driver virtualbox 是默认的，不写就是默认创建虚拟主机
上面尝试在本机创建一个虚拟的名为docker1的docker主机，发现报错

查看另一篇文章

~~~
docker-machine create --driver virtualbox dev

Running pre-create checks...
(dev) No default Boot2Docker ISO found locally, downloading the latest release...
(dev) Latest release for github.com/boot2docker/boot2docker is v19.03.5
(dev) Downloading /root/.docker/machine/cache/boot2docker.iso from https://github.com/boot2docker/boot2docker/releases/download/v19.03.5/boot2docker.iso...
(dev) 0%....10%....20%....30%....40%....50%....60%....70%....80%....90%....100%
Creating machine...
(dev) Copying /root/.docker/machine/cache/boot2docker.iso to /root/.docker/machine/machines/dev/boot2docker.iso...
(dev) Creating VirtualBox VM...
(dev) Creating SSH key...
(dev) Starting the VM...
(dev) Check network to re-create if needed...
(dev) Waiting for an IP...
Waiting for machine to be running, this may take a few minutes...
Detecting operating system of created instance...
Waiting for SSH to be available...
Detecting the provisioner...
Provisioning with boot2docker...
Copying certs to the local machine directory...
Copying certs to the remote machine...
Setting Docker configuration on the remote daemon...
Checking connection to Docker...
Docker is up and running!
To see how to connect your Docker Client to the Docker Engine running on this virtual machine, run: docker-machine env dev
~~~
到这,docker-machine也就创建虚拟docker主机成功了

当然也可能会出现因为网络原因下载boot2docker失败,我们可以直接去github下载,然后放在~/.docker/machine/cache/下
下载地址:https://github.com/boot2docker/boot2docker/releases

创建完成后,我们可以通过docker-machine ls来看一下
~~~
docker-machine ls

NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER     ERRORS
dev       -        virtualbox   Running   tcp://192.168.99.101:2376           v19.03.5   
~~~

* boot2Docker

Boot2Docker是专门用于运行Docker容器的轻量级Linux发行版。它完全从RAM运行，只有约24MB的下载量，并在约5s（YMMV）内启动。[…] Boot2Docker目前已针对开发进行了设计和调整。强烈建议不要将它用于任何类型的生产工作负载


## generic
官方文档：https://docs.docker.com/machine/drivers/generic/ 
driver 使用 generic 可以在现有的VM / Host和SSH创建docker
~~~
docker-machine create \
  --driver generic \
  --generic-ip-address=203.0.113.81 \
  --generic-ssh-key ~/.ssh/id_rsa \
  host_name
~~~
如果docker不在主机上运行，​​它将自动安装。
它将更新主机软件包（apt-get update，yum update...）。
它生成证书以保护docker守护程序。
如果主机使用systemd，它将创建/etc/systemd/system/docker.service.d/10-machine.conf
docker守护程序会重新启动，因此所有正在运行的容器都将停止。
主机名已更新以适合计算机名称。

要创建机器实例，请指定--driver generic，主机的IP地址或DNS名称，以及授权连接到主机的SSH私钥的路径。

| CLI选项                 | 环境变量                | 默认   | 释义                                         |
|-----------------------|---------------------|------|--------------------------------------------|
| --generic-engine-port | GENERIC_ENGINE_PORT | 2376 | 用于Docker Daemon的端口（注意：此标志不适用于boot2docker）。 |
| --generic-ip-address  | GENERIC_IP_ADDRESS  | --   | 主机的必需 IP地址。                                |
| --generic-ssh-key     | GENERIC_SSH_KEY     | --   | SSH用户私钥的路径。                                |
| --generic-ssh-user    | GENERIC_SSH_USER    | root | 用于连接的SSH用户名。                               |
| --generic-ssh-port    | GENERIC_SSH_PORT    | 22   | 用于SSH的端口。                                  |


# docker machine 基本命令

| 指令                                     | 释义                                                                                      |
|----------------------------------------|-----------------------------------------------------------------------------------------|
| docker-machine ls                      | 列出docker-machine管理的docker                                                               |
|[docker-machine env dev](#env)|设置machine机器环境变量|
| docker-machine active                  | 查看哪台计算机处于"活动状态"(如果DOCKER_HOST环境变量指向该计算机，则该计算机被视为活动状态)                                   |
| [docker-machine config dev](#config)   | 配置docker  ：dev是机器名                                                                      |
| [docker-machine inspect dev](#inspect) | 列出机器的详细信息：dev是机器名                                                                       |
| docker-machine kill dev                | 杀死 machine中的机子                                                                          |
| docker-machine rm dev                  | 卸下机器。这将删除本地引用，并在云提供程序或虚拟化管理平台上将其删除。                                                     |
| [docker-machine ssh dev](#ssh)         | 使用SSH登录或在计算机上运行命令                                                                       |
| docker-machine status dev              | machine中机器的状态                                                                           |
| docker-machine start dev               | 开启machine中的机器                                                                           |
| docker-machine stop dev                | 停止machine中的机器                                                                           |
| docker-machine restart dev             | 重新启动机器。通常，这等效于 docker-machine stop,docker-machine start。但是某些云驱动程序尝试实现巧妙的重启，使其保持相同的IP地址。 |
| [docker-machine scp](#scp)             | 使用将文件从本地主机复制到计算机，从一台计算机复制到另一台计算机或从一台计算机复制到本地主机                                          |


<span id="env">

* docker-machine env
~~~
可以通过设置env来指定当前主机连接的是哪台machine机器
$ docker-machine ls
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER     ERRORS
dev       -        virtualbox   Running   tcp://192.168.99.102:2376           v19.03.5   
dev1      -        virtualbox   Running   tcp://192.168.99.101:2376           v19.03.5    
$ eval "$(docker-machine env dev)"
$ docker-machine ls
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER     ERRORS
dev       *        virtualbox   Running   tcp://192.168.99.102:2376           v19.03.5   
dev1      -        virtualbox   Running   tcp://192.168.99.101:2376           v19.03.5  

我们也可以查看本地docker的env
$ env | grep DOCKER
DOCKER_HOST=tcp://192.168.99.102:2376
DOCKER_MACHINE_NAME=dev
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/root/.docker/machine/machines/dev

此时使用docker命令就是在操作名为dev的machine机器,或者machine中连接的远程机器

若要取消这种设置
$ eval "$(docker-machine env -u)"
查看本地docker环境
$ env | grep DOCKER
没有输出,则证明使用docker命令是操作本机
~~~
</span>

<span id="config">

* docker-machine config
~~~
docker-machine config dev \
    --tlsverify \
    --tlscacert="/Users/ehazlett/.docker/machines/dev/ca.pem" \
    --tlscert="/Users/ehazlett/.docker/machines/dev/cert.pem" \
    --tlskey="/Users/ehazlett/.docker/machines/dev/key.pem" \
    -H tcp://192.168.99.103:2376
~~~
</span>


<span id="inspect">

* docker-machine inspect
~~~
在大多数情况下，您可以以一种非常直接的方式从JSON中选择任何字段。也可以选择一部分
获取机器的IP地址：
docker-machine inspect --format='{{.Driver.IPAddress}}' dev
docker-machine inspect --format='{{.Driver}}' dev

虽然这是可用的，但不是很容易理解。因此，有 prettyjson：
docker-machine inspect --format='{{prettyjson .Driver}}' dev

获取一台或多台计算机的IP地址
docker-machine ip dev
docker-machine ip dev1 dev2
~~~
</span>



<span id="ssh">

* docker-machine ssh
~~~
要登录，只需运行docker-machine ssh machinename
docker-machine ssh dev
   ( '>')
  /) TC (\   Core is distributed with ABSOLUTELY NO WARRANTY.
 (/-_--_-\)           www.tinycorelinux.net
docker@dev:~$ 

您还可以通过将docker-machine ssh命令直接附加到命令中来指定要远程运行的命令
docker-machine ssh dev free
              total        used        free      shared  buff/cache   available
Mem:        1013220       54356      651876      290500      306988      651580
Swap:       1195808           0     1195808
~~~
</span>


<span id="scp">

* docker-machine scp
docker-machine scp -r   递归复制,复制文件夹之类的带上此参数
docker-machine scp -d   只传输差异,当传输内容过大时带上此参数,该标志rsync用于传输增量而不是传输所有文件
~~~
machine机器复制文件到本机当前目录
$ docker-machine ssh dev 'echo A file created remotely! >foo.txt'
$ docker-machine scp dev:/home/docker/foo.txt .
foo.txt                             100%   28     0.0KB/s   00:00
$ cat foo.txt
A file created remotely!

拷贝本机文件到machine机器中
$ echo A file created remotely! >bar.txt
$ docker-machine scp bar.txt dev:/home/docker/bar.txt
bar.txt                             100%   28     0.0KB/s   00:00
$ docker-machine ssh dev cat /home/docker/bar.txt
A file created remotely!
~~~
</span>


