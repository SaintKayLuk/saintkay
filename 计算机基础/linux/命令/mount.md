## 挂载命令

linux中将硬盘，u盘，其他文件系统等挂载到本地系统


~~~
mount   [-t 文件系统]   [-L 卷标名]  [-o 特殊选项]  设备文件名  挂载点
~~~

系统启动自动根据 /etc/fstab文件里的内容挂载

### 光盘挂载

* centos 5.x 之前，光盘设备文件名为 /dev/hdc
* centos 6.x 之后，光盘设备文件名是 /dev/sr0

/dev/cdrom 是 /dev/sr0 的软链接，可以作为光盘的设备文件名，推荐使用源文件


~~~
挂载，以 /mnt/cdrom 目录为光盘入口
mount -t iso9660 /dev/cdrom /mnt/cdrom

卸载
umount /mnt/cdrom 或 umount /dev/cdrom
~~~


### U盘挂载

u盘文件名不固定，需要查看u盘的设备文件名
~~~
fdisk -l 
~~~


### NFS文件系统挂载

```
mount -t nfs ip:/挂载点 /本地挂载点
```
例：将192.168.1.11的 /public目录挂载到本地 /mnt目录
```
mount -t nfs 192.168.1.11:/public /mnt
```


### 目录挂载

将一个目录挂载到另一个目录，例如将a目录挂载到b目录，则b目录原有内容隐藏，显示为a目录内容，当umount时候a目录内容重新显示

例：将本地 /mnt 目录挂载到 /tmp 目录
```
mount --bind  /mnt /tmp
```

例：本地 /tmp 目录空间不够，但是又不能换目录。先挂载一个nfs到 /mnt 目录，然后 通过再把 /mnt 目录挂载到 /tmp目录，这样tmp目录用的空间其实就是 nfs的空间