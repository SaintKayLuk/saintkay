nfs一般在unix和类unix中应用比较广泛

## nfs 和 rpc

先启动rpc服务，再启动nfs服务，nfs服务随机使用端口，一般小于1024，然后向rpc注册这些端口，然后rpc记录这些端口，rpc开启111端口
nfs客户端，通过请求nfs服务器的rpc服务的111端口，来获取nfs的端口

* 客户端连接nfs服务步骤
  1. 服务器开rpc服务，开启rpc的111端口
  2. 服务器开nfs服务，随机端口，向rpc服务注册这些端口
  3. 客户端通过本地rpc去请求服务器的rpc服务的111端口
  4. 服务器rpc服务找已注册的nfs服务，并把nfs的端口给客户端
  5. 客户端通过拿到的nfs服务的端口用nfs去连接nfs服务


## 安装nfs服务

nfs服务端，需要用到两个软件包，一个rpc，一个nfs，，centos 6.x之前的rpcbind软件包叫portmap
```
yum install -y rpcbind
yum install -y nfs-utils
```

先启动rpc服务，再启动nfs服务
```sh
#置rpc开机自启并启动 
systemctl enable rpcbind --now

#设置nfs开机自启并启动nfs服务
systemctl enable nfs --now
```

```sh
apt install nfs-kernel-server
```

防火墙放行nfs服务

重新加载防火墙
```
firewall-cmd --reload
```

## 配置文件
nfs配置文件为 /etc/exports 如果不存在新建

/etc/exports 文件格式
```
/etc/exports

共享目录 客户端1(访问权限,用户映射,其他) 客户端2(访问权限,用户映射,其他)

共享目录:     nfs服务器共享给客户端得目录
客户端:       网络中可以访问nfs共享目录的机子
  常见格式:      
    指定ip地址        192.168.1.111
    指定某个网段      192.168.1.0/24，也可以直接192.168.1.0
    指定域名的        www.abc.com
    指定域中所有主机  *.abc.com
    所有主机         *
访问权限:
  共享目录只读:   ro
  共享目录读写:   rw
用户映射选项:
  root_squash:    当客户端为root用户时，映射为nfs服务器端的 nfsnobody用户(默认)
  no_root_squash: 当客户端为root用户时，映射为nfs服务器的root用户
  all_squash:     将所有远程访问的用户都映射为nfs服务器的 nfsnobody用户
  anonuid=xxx:    将远程访问的所有用户都映射为指定uid的匿名用户
  anongid=xxx:    将远程访问的所有用户组都映射为指定gid的匿名组
其他选项:
  sync:         同步，将数据同步写入内存缓冲区和磁盘中，效率低，但可以保证数据一致性
  async:        异步，将数据先保存在内存缓冲区中，再写入磁盘，效率高，但是出现问题时有可能丢失数据


一般 all_squash 结合 anonuid=xxx 和 anongid=xxx 一起使用
```


例：共享nfs服务器的/public 目录给 192.168.1.0 的网段所有用户读写权限，所有访问用户映射为nfsnobody，并异步写入
```
/public 192.168.1.0(rw,all_squash,async)
```

## 共享目录设置

设置共享路径，例如 /home/public  ，如果是以root用户创建的目录，那共享之后，客户端没有办法读写，要修改共享目录的所有者和所有组
安装完nfs之后会在系统生成一个 nfsnobody 用户，把共享目录 /home/public 所有者和所属组改为nfsnobody
```
chown nfsnobody:nfsnobody /home/public
```

配置文件和共享目录设置完之后，重新加载nfs服务，使配置生效
```
systemctl reload nfs
```

查看本地共享目录
```
exportfs
或
showmount -e 本机ip
```

-----

## 常用命令

exportfs命令，修改/etc/exports文件之后，可以通过exportfs命令生效，而不用restart nfs服务或者reload nfs服务
```
exportfs [-aruv]
  -a  全部挂载或卸载/etc/exports中的内容
  -r  重新读取/etc/exports中的内容，并同步更新/etc/exports,/var/lib/nfs/xtab
  -u  卸载单一目录，和-a一起使用时卸载/etc/exports中所有目录
  -v  输出详细信息
```
例：卸载所有共享目录
```
exportfs -au
```

showmount命令，客户端也可使用，可以查看某个ip的共享目录
```
showmount [选项] server
    -e  显示server端所有的共享
    -a  列出所有挂载server的客户端，以即挂载目录，"主机:目录" 方式显示
    -d  列出已被挂载的共享目录
```



## nfs 客户端

* linux端

查看nfs服务端可挂载目录
```
showmount -e nfs服务器ip
```
例：手动挂载，把192.168.1.2服务器的 /public 目录以 nfs 文件系统格式挂载到本地 /mnt 目录，重启生效，
```
mount -t nfs 192.168.1.2:/public /mnt
```


例：自动挂载，修改 /etc/fstab 文件,把 192.168.1.2 服务端的 /public 目录挂载到本地 /mnt/public 目录，重启生效
```
192.168.1.2:/public  /mnt/public       nfs    defaults 0 0
```

* windows端

1. 使用 showmount.exe 查看nfs共享
```
showmount.exe -e 192.168.1.2
```
2. 开启 nfs 服务，win10家庭版需升级到专业版，
```
控制面板 -->  程序和功能 --> 启用和关闭windows功能 --> 启用nfs服务
```
3. 连接nfs服务
```
我的电脑 --> 映射网络驱动器 --> 输入 nfs共享地址\\192.168.1.2\public
```

4. windows客户端使用nfs服务时，会出现中文乱码问题
```
控制面板 --> 区域 --> 管理 --> 更改系统区域设置 --> 打勾 "Beat版，使用Unicode UTF-8提供全球语言支持(U)"

但此操作会使某些国内下载的中文文件乱码
```
