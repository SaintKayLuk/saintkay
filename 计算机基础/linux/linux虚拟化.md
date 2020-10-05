# virtualbox
机子需要开启虚拟化

下载oracle_vbox.asc
~~~
wget -q https://www.virtualbox.org/download/oracle_vbox.asc
rpm --import oracle_vbox.asc
~~~

添加yum源
~~~
cd /etc/yum.repos.d
touch virtualbox.repo
vi virtualbox.repo
~~~
添加如下内容
~~~
[virtualbox]
name=Oracle Linux / RHEL / CentOS-$releasever / $basearch - VirtualBox
baseurl=http://download.virtualbox.org/virtualbox/rpm/el/$releasever/$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://www.virtualbox.org/download/oracle_vbox.asc
~~~
安装VirtualBox
~~~
yum install -y VirtualBox-5.2
~~~


安装完之后，开启linxu 虚拟服务 /sbin/vboxconfig 发现报错
~~~
vboxdrv.sh: Stopping VirtualBox services.
vboxdrv.sh: Starting VirtualBox services.
vboxdrv.sh: Building VirtualBox kernel modules.
This system is currently not set up to build kernel modules.
Please install the gcc make perl packages from your distribution.
Please install the Linux kernel "header" files matching the current kernel
for adding new hardware support to the system.
The distribution packages containing the headers are probably:
    kernel-devel kernel-devel-3.10.0-1062.18.1.el7.x86_64
This system is currently not set up to build kernel modules.
Please install the gcc make perl packages from your distribution.
Please install the Linux kernel "header" files matching the current kernel
for adding new hardware support to the system.
The distribution packages containing the headers are probably:
    kernel-devel kernel-devel-3.10.0-1062.18.1.el7.x86_64

There were problems setting up VirtualBox.  To re-start the set-up process, run
  /sbin/vboxconfig
as root.  If your system is using EFI Secure Boot you may need to sign the
kernel modules (vboxdrv, vboxnetflt, vboxnetadp, vboxpci) before you can load
 them. Please see your Linux system's documentation for more information.
~~~

根据提示我们安装kernel-devel-3.10.0-1062.18.1.el7.x86_64
~~~
yum install -y kernel-devel
~~~
安装完之后重启，重新尝试 /sbin/vboxconfig 我发现还是报错
查看内核版本和安装版本是否一致
~~~ 
uname -r
3.10.0-514.el7.x86_64
ll usr/src/kernels/
3.10.0-1062.18.1.el7.x86_64
~~~
我尝试的时候 我发现不一致，我升级了内核版本 yum update kernel
更新完内核版本需要重启机子生效


继续 /sbin/vboxconfig
发现还是报错
~~~
vboxdrv.sh: Stopping VirtualBox services.
vboxdrv.sh: Starting VirtualBox services.
vboxdrv.sh: Building VirtualBox kernel modules.
This system is currently not set up to build kernel modules.
Please install the gcc make perl packages from your distribution.
This system is currently not set up to build kernel modules.
Please install the gcc make perl packages from your distribution.

There were problems setting up VirtualBox.  To re-start the set-up process, run
  /sbin/vboxconfig
as root.  If your system is using EFI Secure Boot you may need to sign the
kernel modules (vboxdrv, vboxnetflt, vboxnetadp, vboxpci) before you can load
 them. Please see your Linux system's documentation for more information.
~~~

根据错误信息
~~~
yum install -y gcc perl make
~~~

如下显示，成功
~~~
/sbin/vboxconfig

vboxdrv.sh: Stopping VirtualBox services.
vboxdrv.sh: Starting VirtualBox services.
vboxdrv.sh: Building VirtualBox kernel modules.
~~~