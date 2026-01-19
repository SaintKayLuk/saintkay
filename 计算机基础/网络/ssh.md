## 登陆验证模式

* 账户密码
* 密钥对

### 账户密码
```
ssh 用户名@ip
```

例：通过ssh 用root用户登陆192.168.1.1
```
[root@localhost ~]# ssh root@192.168.1.1
```

### 密钥对

```
ssh-keygen [选项]
    -t rsa/dsa  指定加密类型
    -b 数字     指定加密长度，可以使用 1024，2048等
```

1. 本地生成密钥对
```
[root@localhost ~]# ssh-keygen -t rsa -b 2048
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): 
#询问密钥保存位置，默认是 ~/.ssh/id_rsa 不指定其他位置可以直接回车
Enter passphrase (empty for no passphrase):
#询问是否需要对密钥文件加密(加密的是私钥)，默认不加密，若加密后，则调用密钥文件时需要先验证密钥的密码
```   
2. 上传公钥到需要登陆的远程机器，此命令会将公钥copy到 ~/.ssh/authorized_keys 中
```
[root@localhost ~]# ssh-copy-id 用户名@ip
#此用户名是用来登陆远程机器的用户，即需要用什么用户来登陆，然后输出密码即可
```
3. (可选)修改 ~/.ssh/ 和 ~/.ssh/authorized_keys 权限
```sh
chmod 700 ~/.ssh/
chmod 600 ~/.ssh/authorized_keys
```
4. 直接登陆就行，不需要密码
```
[root@localhost ~]# ssh 用户名@ip
```



.ssh目录下的文件
```
authorized_keys         存放公钥，对于其他机器访问此机子,可以存放多个公钥，一行一个
id_rsa                  生成的私钥文件，用于访问其他机子，可以存放多个私钥，-----BEGIN RSA PRIVATE KEY-----开始，-----END RSA PRIVATE KEY-----结束，中间算一个私钥
id_rsa.pub              生成的公钥文件，用于拷贝到其他机子，实现免密登陆
known_hosts             已知的可以免密登陆的机子的信息，保证登陆的是同一台，如果此文件中没有记录，则会询问
```

当一台机子需要被免密登陆时，只需要authorized_keys一个文件，内容就是id_rsa.pub的内容
当一台机子需要免密登陆其他机子时，需要id_rsa，known_hosts两个文件，known_hosts文件会在第一次登陆后生成


## ssh配置文件

ssh server配置文件
```sh
[user1@localhost ~]$ cat /etc/ssh/sshd_config
...
#是否启用密码登陆，yes可以使用账号密码登陆，no不能使用账号密码登陆
PasswordAuthentication yes
...
#root用户是否能够通过ssh远程登陆
PermitRootLogin yes
...
#是否允许使用纯RSA公钥认证
RSAAuthentication yes
#是否允许公钥认证
PubkeyAuthentication yes
...
#监听端口，默认22，为了安全，可以修改为65535以内的万位数端口，登陆时 ssh -p 端口 用户@ip
Port 22
...
#ssh监听ip，有多个网卡时，会有多个ip，可以指定只监听某个ip的端口，即只允许通过指定ip来登陆，默认0.0.0.0监听所有ip
#例如某服务器有2个网卡，并且有2个ip分别是192.168.1.111和192.168.2.222 指定 ListenAddress 192.168.2.222 那只能通过 ssh 用户名@192.168.2.222 来登陆
ListenAddress 0.0.0.0
```


## 源码编译openssh

基于某些不智能的漏洞扫描工具，只会判断大版本号而不判断补丁号，统一认定你的ssh版本为漏洞版本，所以需要源码编译一个高版本的openssh

```sh
# 安装依赖
sudo apt update
sudo apt install -y build-essential zlib1g-dev libssl-dev libpam0g-dev libselinux1-dev pkg-config

# 下载源码
cd /usr/local/src
wget https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-9.9p2.tar.gz
sudo tar -xzf openssh-9.9p2.tar.gz
cd openssh-9.9p2

# 编译并安装
./configure --prefix=/usr --sysconfdir=/etc/ssh --with-pam
make
sudo make install

# 可选：重启 ssh
systemctl restart ssh
```



## 基于ssh的其他协议

### scp
安全的远程传输协议，不同于cp，cp是linux本机拷贝文件，scp是远程拷贝文件
```
#本地向远程服务器拷贝文件
scp [选项] 本地文件/目录 用户名@ip:目录
    -P 端口     (大写P)指定端口，默认是ssh的22端口，如果不是22，则需要显式指定
    -r          复制目录，递归复制整个目录，不加-r是只复制文件
    -q          不显示传输进度条
    -v          详细方式显示输出
    -p          密码

#从远程服务器下载文件
scp [选项] 用户名@ip:文件全路径 本地目录
```

例：把本地root目录下的 test.txt 远程copy到 192.168.1.12 的/tmp 目录下
```sh
scp /root/test.txt root@192.168.1.12:/tmp
```

例：从192.168.1.12上远程下载 root目录下的 abc.txt 文件到本地 /tmp 目录
```sh
scp root@192.168.1.12:/root/abc.txt /tmp
```
### sftp
加密的ftp协议，在ftp协议上加了一层ssh，比ftp更安全，但传输效率比ftp低
```
sftp [选项] 用户名@ip
    选项：
        -oPort=端口     指定端口，默认端口22，如果不是22端口，需要显式指定
    
    交互命令：
        help            查看交互模式下支持哪些命令
        pwd             查看服务器所在路径
        lpwd            查看本机所在路径
        ls              查看服务器当前目录下的文件列表
        lls             查看本机当前目录的文件列表
        put 文件名      将本机指定文件上传到服务器端当前路径下
        get 文件名      将服务器端指定文件下载到本机当前目录下
        rm  文件名      删除服务器端指定文件
        quit/exit       退出sftp交互模式
```