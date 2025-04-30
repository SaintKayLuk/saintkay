

redhat的yum需要注册，替换为centos7的yum来使用

1. 删除原yum
```
rpm -qa|grep yum|xargs rpm -e --nodeps
```

2. 下载rpm包,404则下载最新版本，没有wget通过浏览器下载，上传到redhat
```sh
wget http://mirrors.163.com/centos/7/os/x86_64/Packages/python-iniparse-0.4-9.el7.noarch.rpm
#wget http://mirrors.163.com/centos/7/os/x86_64/Packages/python-urlgrabber-3.10-8.el7.noarch.rpm
wget https://mirrors.163.com/centos/7/os/x86_64/Packages/python-urlgrabber-3.10-10.el7.noarch.rpm
wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-3.4.3-158.el7.centos.noarch.rpm
wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-metadata-parser-1.1.4-10.el7.x86_64.rpm
wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.31-45.el7.noarch.rpm
wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-utils-1.1.31-45.el7.noarch.rpm
```

3. 安装rpm包
```
rpm -ivh --force --nodeps *.rpm
```

4. 添加yum源
```
yum-config-manager --add-repo="http://mirrors.163.com/.help/CentOS7-Base-163.repo"
```

修改配置内容，将文件中的 $releasever 改为 7
```
vi /etc/yum.repos.d/CentOS7-Base-163.repo
:%s/$releasever/7/ge 
```

1. 清除原有缓存，使设置生效
```
clean all       #清理yum缓存，使设置生效
yum makecache   #将服务器上的软件包信息缓存到本地,以提高搜索安装软件的速度
```

6. 禁用通知
```
vi /etc/yum/pluginconf.d/subscription-manager.conf

[main]
enabled=1
```

enabled=1 改为 enabled=0 ，禁用通知