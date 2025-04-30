## 版本变迁

```
2.2 --> 需要手动加载的一个外部模块
2.4 --> 直接写道内核的一个模块
2.6 --> 成为了一部分Linux发行版的内核的一部分
```

成为linux内核的一部分的软件哪一个都不简单，都非常牛逼。



## 安全上下文

```
用户:角色:类型标识符
```



## 配置文件

```sh
cat /etc/selinux/config

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected. 
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted 
```

* enforcing：开启selinux
* permissive：提示，但不限制
* disabled：禁用selinux
---
* targeted
* minimum
* mls

修改 /etc/selinux/config 来永久关闭或者开启selinx或修改策略需要重启才生效







## 常用命令

```sh
sestatus        查看selinux是否开启
getenforce      查看selinux是否开启

setenforce [Enforcing/Permissive]   临时修改，Enforcing相当于1
setenforce [1/0]                    临时修改


ll -Z           查看selinux的 用户:角色:类型标识符
```

更改文件/文件夹的selinux的安全上下文
```
chcon [选项] [-u 用户] [-r 角色] [-t 类型] 文件/文件夹
    
选项
    -R  递归更改
    -v  打印详细过程
```

还原 selinux type
```
restorecon [选项] 文件/文件夹

选项
    -R  递归更改
    -v  打印详细过程
```


## selinux 布尔值

精准控制 selinux 对某个软件的某个选项的保护

查看selinux布尔值
```
getsebool [选项]
    -a  查看所有
    某个选项
```

例：查看 zabbix_run_sudo 的开关
```
getsebool -a | grep zabbix_run_sudo
getsebool zabbix_run_sudo
```


设置selinux布尔值
```
setsebool [-NPV] 选项 [on/off]/[1/0]

    -N  
    -P  写入文件，永久生效，否则重启失效
    -V  
```

例：临时设置 zoneminder_anon_write 的selinux布尔值开启
```sh
setsebool zoneminder_anon_write 1
```