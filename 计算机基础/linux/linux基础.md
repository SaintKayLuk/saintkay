### 注意事项

1. linux严格区分大小写
2. linux一切皆文件
3. linux不靠扩展名区分文件类型，添加扩展名为了好区分
    - 压缩包，常见压缩文件名：*.gz *.bz2 *.zip *.tar.gz *.tar
    - 二进制软件包：*.rpm
    - 程序文件：*.sh *.c
    - 网页文件：*.html *.php

4. linux中所有存储设备必须挂载之后才能使用
5. windows下的程序不能直接在linux中使用

### 服务器注意事项

1. 最好重启，不要关机
2. 重启前，中止正在执行的服务
3. 重启命令，最好用shutdown -r now，之前可以多次sync同步数据
4. 设置防火墙规则，不要把自己踢出去
5. 合理密码规范
6. 合理分配权限
7. 定期备份重要数据和日志

### 目录结构

一级目录
~~~
/bin            存放所有用户都可以使用的“必要”命令，/usr/bin 目录软链接
/boot           存放开机启动加载程序的核心文件
/dev            设备文件目录
/etc            主机或系统配置文件目录
/root           管理员主目录
/home           普通用户目录
/lib            需要共享的函数库与kernel模块
/media          移动存储设备挂载点
/mnt            临时挂载点
/opt            额外安装的应用程序目录，此目录没有出来之前，软件习惯安装在/usr/local
/tmp            临时文件目录
~~~

/usr 下二级目录
~~~
/usr/local          一般软件安装在此目录，
/usr/share          应用程序资源文件，如帮助文档
/usr/src/kernels    内核源码目录

~~~

/var 下二级目录
~~~
/var/log            系统日志文件目录
/var/run            运行中的应用程序pid
/var/mail           用户的邮箱目录
/var/spool          应用程序列队文件目录
/var/spool/cron     系统的定时任务列队目录
~~~

### 常用命令

1. 提示符  

~~~
 [root@localhost ~]#
 root： 代表当前登陆用户
 @：分隔符，没有意义
 localhost: 当前主机名简写
 ~：当前所在目录
 #：命令提示符，超级用户是#，普通用户是$
~~~

#### 文件目录命令

~~~shell
ls          显示目录下内容 -l，长格式
pwd         显示当前路径
cd          切换目录
mkdir       创建目录
rmdir       删除空目录
touch       创建文件
echo        输出内容或者写入内容

                echo "xxx" > 123.txt,覆盖内容
                echo "xxx" >> 123.txt ,追加内容
                     

rm          删除文件或者目录
stat        查看目录或文件详细信息
cat         查看文件内容

more        交互显示，分屏
less        交互显示，分行，主要用more就行

                空格：向下翻页
                按b，向上翻页
                回车键，向下滚动一行
                /字符串，查找指定字符串
                按q，退出

head        默认显示前10行，-n 从头开始显示的行数
tail        默认显示后10行，-n 从末尾开始显示的行数




cp [选项] 源文件 目标文件       
    -r  递归复制，用于复制目录下所有内容
    -p  复制所有属性，比如权限等
    -d  用于复制软链接，源文件是软链接，则复制出来的目标文件也为软链接

mv          移动文件或目录，在相同目录下操作可改名
~~~

#### ln

~~~
ln [选项] 源文件 目标文件              链接，参数需要绝对路径
    -s  建立软链接，不加s建立的是硬链接
    -f  强制，如果目标文件已存在，则删除目标文件再重新生成链接文件


例：查看硬链接与软链接,abc_s是abc的软链接，abc2是abc的硬链接，或者abc是abc2的硬链接
ls -li
256132 lrwxrwxrwx 1 root root        2 9月  11 10:05 abc_s -> abc
256137 -rw-r--r-- 2 root root      750 9月  11 09:35 abc
256137 -rw-r--r-- 2 root root      750 9月  11 09:35 abc2
~~~

##### 硬链接

*  源文件和硬链接文件拥有相同的 inode 和 block
*  修改任一个文件，另一个都改变
*  删除任一个文件，另一个都能使用，链接数减1，如上 第三列的2，代表2个链接，删除最后一个硬链接或者源文件，链接数为0时，同时删除block
*  不能链接目录
*  不能跨分区

##### 软链接

* 软链接和源文件拥有不同的 inode 和 block
* 修改任一个文件，另一个都改变
* 删除软链接，源文件不受影响，删除源文件，软链接失效，类似于windows的快捷方式
* 软链接没有数据，只保存源文件的 inode ，无论源文件大小多少，软链接大小不变
* 软连接为最大权限 lrwxrwxrwx ，最终访问权限需要参考源文件的权限
* 可以连接目录
* 可以跨分区



#### 帮助命令

~~~ shell
man         man xxx   查看xxx命令的内容
info        info xxx  完整的帮助
help        help xxx  只能获取shell内置命令帮助
--help      xxx --help
~~~

#### 搜索命令


~~~shell
查找命令，不能查找文件
whereis     查找命令位置和帮助文档位置
which       查找命令位置，如果有别名加上别名显示
~~~



~~~shell
只能查找文件名,配置文件位于 /etc/updatedb.conf
locate      按照数据库搜索，数据库位于 /var/lib/mlocate/mlocate.db 但数据库不一定实时更新，可重新登陆，或者 updatedb
~~~

##### find命令
~~~shell
find    搜索路径    [选项]    搜索内容
~~~
1. 按文件名搜索
~~~shell
find    搜索路径    [选项]    文件名
    -name   按文件名搜索
    -iname  按文件名搜索，不区分大小写
    -inum   按i节点搜素
    -size   按大下搜索

例：
find . -name abc    搜索当前目录下的文件名为abc的文件
~~~

2. 按大小搜索
~~~shell
find    搜索路径    -size    大小
    -size  +|- 大小

例：
find . -size +100k     搜索当前路径下大于100k的文件

c   字节
k   kb
M   Mb
G   Gb
~~~

3. 按修改时间
~~~shell
find    搜索路径    [+|-]  时间  
    -atime  按文件访问时间
    -mtime  按文件修改时间
    -ctime  按文件创建时间

例子：
find . -mtime -5    当前路径下5天内修改过的文件
-5  代表5天内修改的文件
5   代表5-6天之间修改的文件
+5  代表6天前修改的文件 
~~~

4. 按权限
~~~shell
find 搜索路径   -perm   [+|-] 
~~~

6. 按文件类型
~~~shell
find    搜索路径    -type  [d|f|l]
    -type d 搜索目录
    -type f 搜索文件
    -type l 搜索软链接
~~~


##### grep
在文件中搜索符合条件的字符串
~~~shell
grep 搜索内容   [选项]  文件名
    -i 不区分大小写
    -n 输出行号
    -v 反向搜索(取反)
    --color=auto
~~~


#### 通配符
用于匹配文件名，完全匹配，find 命令搜索文件命名中可以使用通配符
~~~
?   匹配一个任意字符
*   匹配0个或多个任意字符，也可以匹配任意内容
[]  匹配中括号中任意一个字符，[abc] 代表匹配a,b,c其中一个，一个中括号代表匹配一个字符
    [-]中间加 - ，例如[a-z],代表一个小写字母
    [^] 取反，例如[^0-9],代表匹配一个不是数字的字符
~~~

#### 正则表达式
用于匹配字符串，包含匹配

~~~
?   匹配前一个字符重复0次或1次          --只能用egrep命令来使用
*   匹配前一个字符重复0次或任意多次
[]  匹配中括号中任意一个字符，[abc] 代表匹配a,b,c其中一个，一个中括号代表匹配一个字符
    [-]中间加 - ，例如[a-z],代表一个小写字母
    [^] 取反，例如[^0-9],代表匹配一个不是数字的字符
^   匹配行首
$   匹配行尾
~~~

#### 管道符
前一个命令的输出结果(作为文本流) 作为下一个命令的操作对象，可以多个管道符一起使用
~~~
命令1 | 命令2 | 命令3 | ...

例1：ll /etc | more                             分屏显示/etc目录下的子目录和文件
例2：ll /etc | grep xxx                         显示/etc下面的包含 xxx 的子目录或文件
例3：netstat -an | grep "ESTABLISHED" | wc -l   wc：统计命令，统计网络状态为 ESTABLISHED 的连接
~~~


#### 命令别名
别名优先级大于系统命令，即定义相同命令，会使用别名
~~~
alias               查看系统中的别名
alias 别名='原命令'  临时设置别名，重启失效

写入用户环境变量文件 ~/.bashrc
~~~


#### 补充命令
~~~
Tab         命令或文件补全
Ctrl+A      把光标移动到行首
Ctrl+E      把光标移动到行尾
Ctrl+L      清屏，相当于clear
Ctrl+C      强制终止当前命令
Ctrl+U      删除或者剪切光标之前的命令
Ctrl+Y      粘贴 Ctrl+U 剪切的内容
~~~


#### 压缩解压缩命令

##### .zip
压缩
~~~
zip  [选项]  压缩文件  源文件或者源目录(可以有多个)
    -r 压缩目录

例1：把当前目录下的 abc1 和 abc2 文件压缩为 abc.zip 压缩文件
zip abc.zip abc1 abc2

例2：把 /xxx 目录压缩为 abc.zip 压缩文件
zip abc.zip -r /xxx
~~~

解压
~~~
unzip  [选项]  压缩包名
    -r 指定压缩位置

例：把 abc.zip 压缩文件解压到 /tmp 目录下
unzip -r /tmp/ abc.zip
~~~
##### .gz

压缩完默认删除源文件,不会打包目录
~~~
gzip  [选项]  源文件
    -c 将压缩数据输出到控制台，或者输出到其他文件
    -d 解压缩   等同于 gunzip命令，推荐使用 gzip -d
    -r 压缩目录，但是不会打包目录，会将目录下的文件都压缩
~~~

##### .bz2

不能压缩目录，能保留源文件
~~~
bzip2  [选项]  源文件
    -d 解压缩       等同于 bunzip2 命令
    -k 压缩完，保留源文件
    -v 显示压缩的详细信息
~~~

##### .tar

打包，但是不能压缩
~~~
tar  [选项]  源文件或目录
    -c      打包
    -x      解打包
    -f      压缩包名
    -v      显示打包过程
    -t      测试，不解打包，只查看包有哪些文件
    -C 目录 （大C）指定解打包位置，要跟在包后面

例：把 abc bcd 打包进 abc.tar
tar -cvf abc.tar abc bcd 

例：解包 abc.tar 到 /tmp 目录下
tar -xvf abc.tar -C /tmp 

例：只解包中的某个或多个文件和目录到 /tmp 目录下，abc.tar 中有abc bcd，只解bcd
tar -xvf abc.tar -C /tmp bcd
~~~

##### .tar.gz 和 .tar.bz2

.tar 格式只能打包，不能压缩，和 .gz 或 .bz2 格式一起使用，即能打包也能压缩
~~~
tar 命令同上
    -z 压缩或者解压 .tar.gz 格式 
    -j 压缩或者解压 .tar.bz2 格式

例：解压 .tar.gz 包
tar -zxvf abc.tar.gz

例：将 abc bcd 文件 打包压缩成 abc.tar.bz2
tar -jcvf abc.tar.bz2 abc bcd
~~~

#### 关机重启命令


~~~
sync        数据同步，刷新文件系统缓冲区
shutdown    最安全的关机，重启命令
    -h  关机
    -r  重启
    now 立刻
    -c  取消已经执行的shutdown命令
例：shutdown -r 5:00    在5点重启，不建议指定时间重启

reboot      重启
halt        关机，不建议使用
poweroff    关机，不建议使用
init        运行级别的命令，不建议使用 init 0 之类的    
~~~



#### 网络命令

~~~
ifconfig    查看网卡信息
ping        探测网络连接，后面跟 域名或者ip
    -b  后面跟广播地址，用于对整个网段进行探测
    -c  探测次数
    -s  指定探测包的大小

netstat
    -a      所有网络状态，包括socket
    -c 秒数 每隔几秒刷新一次网络状态      例：netstat -c 5  
    -n      使用ip地址和端口号显示，不使用域名和服务名
    -p      显示pid和程序名
    -t      显示tcp协议端口得连接状况
    -u      显示udp协议端口得连接状况
    -l      仅显示监听状态得连接
    -r      显示路由表

例：查看tcp监听状态的连接
netstat -ntl
例：查看网关ip
netstat -rn
~~~

linux终端
~~~
6个本地字符终端 tty/1-6     alt+F1+[1-6]
本地图形终端    tty7
远程终端        pts/0-255
~~~

~~~
write   给指定终端发信息
write 用户名 终端号
例：write root pts/1

wall    给所有终端用户发信息
例：wall 回车，输入内容，ctrl+D 发送，或者 wall "需要发送的消息"


mail    查看/发送 邮件
    -s  指定邮件标题

例：把 /root/anaconda-ks.cfg 文件发送给root用户
mail -s "test mail" root < /root/anaconda-ks.cfg    

例：查看邮件  
[user1@VM-0-4-centos ~]$ mail
...
    1 root                  Mon Aug 24 17:53  19/649   "test1 mail"
>U  2 root                  Mon Aug 24 17:57  19/650   "test2 mail"
 N  3 root                  Mon Aug 24 17:59  18/640   "test3 mail"

第一列 U(unread)代表未读，N(new)代表新邮件
第二列邮件编号，输入对应邮件编号 读邮件内容

h           查看邮件列表
d 邮件编号   删除对应邮件
quit        退出，并保存操作
exit        退出，不保存操作
~~~


#### 历史日志

##### w 和 who
查看 /var/run/utmp 文件
~~~
[root@localhost ~]# w

10:18:14 up 8 days, 17:08,  2 users,  load average: 0.04, 0.06, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    122.233.166.48   09:59    6.00s  0.12s  0.12s -bash
root     pts/1    122.233.166.48   09:59   18:22   1.30s  1.28s top

10:18:14:           系统当前时间
up 8days, 17：08：  系统持续运行时间
2 users：           登陆用户数
load average：      系统在1分钟，5分钟，15分钟之前的平均负载
~~~

who 显示内容较少



##### last
查看 /var/log/wtmp 文件 ，查看系统登陆过的用户，包括正在登陆中
~~~
[root@localhost ~]# last
~~~


##### lastlog
查看 /var/log/lastlog 文件，查看系统中所有用户最后一次登陆时间，有登陆ip的表示正在登陆中
~~~
[root@localhost ~]# lastlog
用户名           端口     来自             最后登陆时间
root             pts/1    122.233.166.48   四 8月 27 09:59:52 +0800 2020
bin                                        **从未登录过**
...
user1            pts/2                     一 8月 24 17:43:57 +0800 2020
~~~


##### lastb
查看 /var/log/btmp 文件，记录错误登陆信息日志,即密码输错的记录
~~~
[root@localhost ~]# lastb

user     ssh:notty    51.116.231.232   Tue Aug 18 17:28 - 17:28  (00:00)    
user     ssh:notty    51.116.231.232   Tue Aug 18 17:28 - 17:28  (00:00)    
test     ssh:notty    51.116.231.232   Tue Aug 18 17:28 - 17:28  (00:00)    
test1    ssh:notty    51.116.231.232   Tue Aug 18 17:28 - 17:28  (00:00) 
...
~~~


#### 挂载命令

~~~
mount   [-t 文件系统]   [-L 卷标名]  [-o 特殊选项]  设备文件名  挂载点
~~~

系统启动自动根据 /etc/fstab文件里的内容挂载

光盘挂载

* centos 5.x 之前，光盘设备文件名为 /dev/hdc
* centos 6.x 之后，光盘设备文件名是 /dev/sr0

/dev/cdrom 是 /dev/sr0 的软链接，可以作为光盘的设备文件名，推荐使用源文件


~~~
挂载，以 /mnt/cdrom 目录为光盘入口
mount -t iso9660 /dev/cdrom /mnt/cdrom

卸载
umount /mnt/cdrom 或 umount /dev/cdrom
~~~


U盘挂载

u盘文件名不固定，需要查看u盘的设备文件名
~~~
fdisk -l 
~~~