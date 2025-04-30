## systemd

linux 通过 systemd 来控制服务，除了systemd 的 *.service 配置文件以外
systemd 还兼容 SysV init 脚本：/etc/rc.d/init.d/ 或 /etc/init.d/

systemd 具有向后兼容性，可以通过 systemctl 命令来管理这些脚本。
例如，如果没有对应的 .service 文件，而有一个 /etc/init.d/sshd 脚本，你可以使用 systemctl start sshd 来启动服务。


**检查服务单元文件和脚本的存在性**

如果以下都不存在，则此服务没有被systemd管理
```sh
#检查/etc/systemd/system/
ls /etc/systemd/system/xxx.service
#检查/usr/lib/systemd/system/
ls /usr/lib/systemd/system/xxx.service

#检查 /etc/rc.d/init.d/ 或 /etc/init.d/
ls /etc/rc.d/init.d/xxx
# 或者
ls /etc/init.d/xxx
```



对于支持 systemd 的服务，在安装得时候，会自动在/usr/lib/systemd/system目录添加一个 xxx.service 配置文件。


启动一个服务 systemctl start xxx 调用 usr/lib/systemd/system/xxx.service 
```sh
systemctl start xxx
```


设置开机自启 systemctl enable xxx 会在 /etc/systemd/system 目录下添加一个软链接
这是因为开机时，Systemd只执行/etc/systemd/system目录里面的配置文件
```sh
systemctl enable xxx
```


查看 xxx 服务的状态，一下为kdump.service服务为例
```
[root@localhost ~]# systemctl status kdump.service
● kdump.service - Crash recovery kernel arming
   Loaded: loaded (/usr/lib/systemd/system/kdump.service; enabled; vendor preset: enabled)
   Active: active (exited) since 五 2021-09-17 16:52:18 CST; 5 days ago
 Main PID: 5822 (code=exited, status=0/SUCCESS)
   CGroup: /system.slice/kdump.service

9月 17 16:52:14 localhost.localdomain systemd[1]: Starting Crash recovery kernel arming...
9月 17 16:52:18 localhost.localdomain kdumpctl[5822]: kexec: loaded kdump kernel
9月 17 16:52:18 localhost.localdomain kdumpctl[5822]: Starting kdump: [OK]
9月 17 16:52:18 localhost.localdomain systemd[1]: Started Crash recovery kernel arming.


第一行：       服务名，以及描述
Loaded：       配置文件的位置，是否设为开机启动
Active：       服务状态
Main PID：     主进程ID
Status：       服务自己提供的状态显示
CGroup：       应用的所有子进程
最后几行：     应用的日志
```


https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html




### systemctl


#### 查看服务
```sh
# 查看系统状态
systemctl status     
# 查看某个服务的状态   
systemctl status application.service    
```

以下方式主要用于脚本中检查服务状态
```sh
# 显示某个 Unit 是否正在运行
systemctl is-active application.service
# 显示某个 Unit 是否处于启动失败状态
systemctl is-failed application.service
# 显示某个 Unit 服务是否建立了启动链接
systemctl is-enabled application.service
```

#### 启动服务
```sh
# 立即启动一个服务
systemctl start application.service
# 立即停止一个服务
systemctl stop application.service
# 重启一个服务
systemctl restart application.service
# 重新加载一个服务的配置文件
systemctl reload application.service
# 重载所有修改过的配置文件
systemctl daemon-reload
```

#### 服务配置文件


**用户配置文件目录：/etc/systemd/system/**
这个目录用于存放用户创建或覆盖的服务单元文件。
用户在这里创建或修改的服务单元文件会优先于系统级别的服务单元文

**系统配置文件目录：/usr/lib/systemd/system/** 
这个目录用于存放系统级别的服务单元文件，通常由软件包管理器安装。
用户不应该直接修改这个目录中的文件，因为它们可能会在软件包更新时被覆盖。


```sh
# 列出所有配置文件
systemctl list-unit-files [选项]
    --type=service    #列出service类型的服务
    --type=socket     #列出socket类型的服务


#这个列表显示每个配置文件的状态，一共有四种。

enabled：已建立启动链接
disabled：没建立启动链接
static：该配置文件没有[Install]部分（无法执行），只能作为其他配置文件的依赖
masked：该配置文件被禁止建立启动链接
```
### 配置文件


1. 大小写敏感
2. 每个区块内部是一些等号连接的键值对
3. 键值对的等号两侧不能有空格
```conf
[Unit]
Description=#简短描述
Documentation=#文档地址，可以是 URL 或文件路径。
Documentation=#文档地址，可以存在多个，一个写文件路径，一个写 URL
Requires=   #定义该服务依赖的其他单元，如果这些单元无法启动，该服务也会失败
Before=     #定义服务启动的顺序，表示该服务要在指定目标服务之前启动
After=      #定义服务启动的顺序，表示该服务要在指定目标服务之后启动。
Wants=      #定义该服务希望启动的其他单元，但这些单元失败不会导致该服务失败
Conflicts=  #定义该服务与哪些单元冲突，不能同时运行，启动当前服务时会停止冲突的单元
BindsTo=    #定义服务绑定到指定单元。如果绑定的单元停止或失败，当前服务也会停止


[Service]
Type=simple #指定服务的启动类型
ExecStart=/usr/bin/my-service --option  #指定启动服务的命令 systemctl start 
ExecStop=/usr/bin/my-service --stop     #指定停止服务的命令
ExecReload=/usr/bin/my-service --reload #指定重新加载服务配置的命令
Restart=no      #指定服务在退出后的重启策略、
RestartSec=5    #指定重启服务前的等待时间（秒）。
User=myuser     #指定以哪个用户身份运行服务
Group=mygroup   #指定以哪个组身份运行服务。
Environment="VAR1=value1" "VAR2=value2" #定义环境变量，可以指定多个变量
WorkingDirectory=/var/lib/my-service    #指定服务的工作目录


[Install]
WantedBy=multi-user.target  #指定该服务所属的目标，表示在该目标下该服务是“想要的”
RequiredBy=                 #指定该服务所属的目标，表示在该目标下该服务是“必须的”
Also=                       #指定相关的单元文件，在启用或禁用该服务时一起启用或禁用。
Alias=                      #为该服务创建一个别名，可以用该别名来管理服务
```

* Type类型
  * simple（默认）：ExecStart 启动的进程是服务的主进程。
  * forking：ExecStart 启动的进程会分叉子进程，父进程会退出。
  * oneshot：服务在完成一次性任务后退出。
  * notify：ExecStart 启动的进程会向 systemd 发送通知。
  * idle：ExecStart 启动的进程会在所有其他任务完成后运行。

* Restart类型
  * no：不重启（默认）。
  * always：总是重启。
  * on-failure：仅在非零退出代码时重启。
  * on-abnormal：仅在非正常退出时（如信号终止）重启。
  * on-watchdog：仅在超时情况下重启。
  * on-abort：仅在任务被非捕获信号终止时重启。


在service文件中，有些选项可以指定已有的target，如 After、Wants、WantedBy等
* target选项
  * multi-user.target
    * 表示多用户模式，没有图形界。这是大多数服务器的默认目标
    * 等同于传统的运行级别 3
    * 示例：大多数后台服务（如数据库、Web 服务器等）通常会使用此目标
  * graphical.target
    * 表示多用户模式，并且有图形界面。这是桌面系统的默认目标
    * 等同于传统的运行级别 5
    * 示例：桌面环境相关的服务（如 Display Manager）会使用此目标
  * basic.target
    * 表示系统初始化的基本目标，大部分系统服务都可以在此目标之后启动
    * 这是所有其他目标的基础
    * 示例：一些基础系统服务可能会使用此目标
  * default.target
    * 通常是 graphical.target 或 multi-user.target 的别名
  * sysinit.target
    * 在 basic.target 之前运行
  * network.target
    * 表示网络已经启动并可用的目标
    * 需要网络支持的服务（如 DHCP 客户端）会使用此目标。
  * network-online.target
  * remote-fs.target
    * 表示远程文件系统已经挂载的目标
    * 依赖于远程文件系统的服务可能会使用此目标
  * shutdown.target

---
例：sshd.service
```conf
[Unit]
Description=OpenSSH server daemon
After=network.target

[Service]
ExecStart=/usr/local/sbin/sshd -D
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
