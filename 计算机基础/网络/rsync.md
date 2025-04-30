## rsync

* 使用ssh协议
* 使用rsync协议


```
rsync [选项] [本地目录/目标目录] [本地目录/目标目录]
    -a          递归传输，包括所有属性
    -v          显示传输过程
    -q          只显示错误信息
    -z          压缩传输
    --delete    同步时，删除比服务多的文件(删除源地址没有，目标地址有的文件，相当于删除也同步)
    --exclude   排除指定目录同步，不能写绝对路径 
```

### ssh协议

和 scp 类似

```sh
#将远端服务器目标下所有文件同步到本地目录
rsync -avz root@192.168.2.61:/rsync/ /rsync/

#将本地目录同步到远端服务器
rsync -avz /rsync/  root@192.168.2.61:/rsync/
```

和scp一样，每次同步都需要输入密码，免密同ssh免密登陆

### rsync协议

#### 准备工作

1. 远端服务器安装 rsync (默认安装) 
```sh
yum install -y rsync
```


2. 配置文件 /etc/rsyncd.conf
```conf
# /etc/rsyncd: configuration file for rsync daemon mode

# See rsyncd.conf man page for more options.

# configuration example:

# uid = nobody
# gid = nobody
# use chroot = yes
# max connections = 4
# pid file = /var/run/rsyncd.pid
# exclude = lost+found/
# transfer logging = yes
# timeout = 900
# ignore nonreadable = yes
# dont compress   = *.gz *.tgz *.zip *.z *.Z *.rpm *.deb *.bz2

# [ftp]
#        path = /home/ftp
#        comment = ftp export area


#这里自己添加一个模块
[web]
	comment = xxx
	path = /rsync
	read only = false
	fake super = yes
```
3. 修改同步文件夹权限
```
chown nobody:nobody /rsync
```

4. 启动 rsync 服务
```sh
systemctl start rsyncd
```


#### 同步操作

远程同步目录要写模块名，例如上面设置的 web ，指向 /rsync 目录，相当于同步 /rsync

远程同步到本地
```sh
#两种写法
rsync -avz  rsync://root@192.168.2.61/web /rsync/
rsync -avz  root@192.168.2.61::web /rsync/
```

本地同步到远程
```sh
rsync -avz /rsync/ root@192.168.2.61::web
rsync -avz /rsync/ rsync://root@192.168.2.61/web
```

本地两个文件夹同步，/test 文件夹同步到 /test1 文件夹，必须是绝对路径
```sh
rsync -avz /test/ /test1/
```

同步 /test 到 /test1 ，但是排除 /test/abc 目录
```
rsync -avz --exclude="abc" /test/ /test1/
```


## 实时同步

### 单向同步(rsync+inotify)

```
源地址 -- 推送 --> 目标地址
```

在源地址安装 rsync 和 inotyfy
```sh
yum install -y epel-release
yum install -y rsync inotify-tools
```

```
inotifywait [选项] 文件/目录 [文件/目录] ...
    Options
        -m/--monitor    持续监听，没有此选项，监听一次就退出
        -r/--recursive  递归监听目录
        -q|--quiet    	仅打印事件
        -qq             什么都不打印
        -e/--event      监听事件，不写则监听所有事件

    Events
        modify		修改文件或者目录
        attrib		文件或者目录权限改变
        move		从监听目录中移出或者移入到监听目录
        create		创建文件或者目录
        delete		删除文件或者目录
```

例：持续监听 /rsync 目录和 /rsync2 目录的创建和删除动作
```sh
#多个监听动作用 , 分隔
#多个目录用空格分隔
inotifywait -mrq -e create,delete /rsync/ /rsync2/
```

单向同步脚本，源端执行
当源端 /rsync 目录下有新增和删除文件或者目录动作，则发起rsync 同步操作
```sh
#!/bin/bash
a="inotifywait -mrq -e create,delete /rsync/"
b="rsync -aqz --delete /rsync/ rsync://root@192.168.2.10/web"

$a | while read directory event file; do
    $b
done
```

### 双向同步 

#### rsync+inotify

192.168.2.10的 /rsync 目录和 192.168.2.61 的 /rsync 目录实现双向同步
单向同步的脚本在两边都执行一遍

192.168.2.10
```sh
#!/bin/bash
a="inotifywait -mrq -e create,delete /rsync/"
b="rsync -aqz --delete /rsync/ rsync://root@192.168.2.61/web"

$a | while read directory event file; do
    $b
done
```


192.168.2.61
```sh
#!/bin/bash
a="inotifywait -mrq -e create,delete /rsync/"
b="rsync -aqz --delete /rsync/ rsync://root@192.168.2.10/web"

$a | while read directory event file; do
    $b
done
```

**权限问题**
因为rsync默认使用nobody用户，即源端文件传输到目标端 用户和用户组都会变成 nobody
可修改 /etc/rsyncd.conf 如下
```conf
uid = root
gid = root
```

#### unison+inotify 

...




