# vsftp

服务端软件：vsftpd
客户端端口：ftp
服务名：vsftpd

## vsftp连接类型


* 21(传输ftp命令)
* 20(用于数据传输)


## vsftp工作模式

* 主动模式(port模式)
* 被动模式(passive模式)


主动模式：客户端的随机端口和服务端地20端口进行数据传输
```
ftp客户端               ftp服务端

登陆ftp服务器   <--->   21端口
    ↓
    ↓随机开放端口
    ↓
 PORT命令       --->    21端口
    ↓                    ↓
    ↓                    ↓调用20端口
    ↓                    ↓
  随机端口  <-数据传输-> 20端口

```


被动模式：客户端的随机端口和服务端的随机端口进行数据传输
```
ftp客户端               ftp服务端

登陆ftp服务器   <--->   21端口
    ↓           
  PASV命令      --->    21端口
    ↓                     ↓
    ↓随机开放端口          ↓随机开放指定范围内端口(默认1023-65535)
    ↓                     ↓
  随机端口  <-数据传输-> 随机端口


```

## vsftp传输模式

* binary：不对数据进行任何处理
* ASCII：进行文本传输时，自动适应目标操作系统的结束符，回车符等

切换方式：在 ftp> 提示符下输入 ascii 切换到 ACSII方式，输入 bin 切换到binary方式



## 登陆方式

### 匿名用户

用户名称：ftp 和 anonymous
用户密码：无密码
工作目录：/var/ftp
默认权限：默认可下载，不能上传

### 本地用户

用户名称：本地用户(/etc/passwd)
用户密码：本地密码(/etc/shadow)
工作目录：/home/xxx
默认权限：最大权限(drwx------)

### 虚拟用户

使用本地用户作为虚拟用户的映射用户
每个虚拟用户单独设置权限

用户名称：自建
用户密码：自建
工作目录：挂载本地一个用户的家目录
默认权限：同匿名用户权限一致



## 配置文件

```conf
anonymous_enable=YES            #启动匿名访问
anon_umask=022                  #匿名用户umask(默认为077)
anon_root=/var/ftp              #匿名用户的根目录
anon_upload_enable=YES          #匿名用户能否上传
anon_mkdir_write_enable=YES     #匿名用户能否创建目录
anon_other_write_enable=YES     #匿名用户能否有其他写入权限(删除，覆盖，重命名)
anon_max_rate=0                 #匿名用户最大传输速率，(默认为0为不限速，单位 bytes/s）
no_anon_password=NO             #使用匿名登陆时，是否询问密码

dirmessage_enable=YES           #启用后，使用者第一次进入目录，如果目录下有 .message 这个文件，则会提示这个文件内的内容，即目录欢迎语
message_file=.message           #设置目录消息文件(默认为 .message)
banner_file=/etc/vsftpd/banner  #登陆欢迎语
ftpd_banner="Welcome ..."       #登陆欢迎语，设置的是字符串，如果过长可以使用banner_file选项

local_enable=YES                #启用本地用户
write_enable=YES                #本地用户是否有w权限
local_umask=022                 #本地用户umask(默认077)
local_root=/home/xxx            #设置本地用户登陆的根目录，默认是自己的家目录
chroot_local_user=YES           #设置将本地用户限制在家目录，为NO可向上切换到/目录
allow_writeable_chroot=YES      #当用户被限制在家目录下时，则家目录不能拥有w权限，或可以添加此配置
chroot_list_enable=YES          #开启将本地用户登陆ftp被限制在家目录下
chroot_list_file=/etc/vsftpd/chroot_list  #白名单，此白名单内的用户不受 chroot_list_enable 参数影响，即可随意切换目录(默认不存在，需自己创建)
local_max_rate=0                #限制本地用户最大传输速率
file_open_mode=0755             #(默认0666)

#默认使用二进制上传，不开启ascii模式情况下，服务器假装允许ascii模式上传，实则忽略
ascii_upload_enable=YES         #是否启动ASCII模式上传数据(默认为NO)
ascii_download_enable=YES       #是否启动ASCII模式下载数据(默认为NO)

tcp_wrappers=YES/NO(YES)            #启动tcp_wrappers
userlist_enable=YES/NO(NO)          #是否启用用户访问
userlist_deny=YES/NO(YES)           #设置user_list文件中的用户是否能访问ftp
userlist_file=/etc/vsftpd/user_list #用户访问控制权限文件

pam_service_name=vsftpd             #pam文件，即 /etc/pam.d/vsftpd
guest_enable=YES                    #开启虚拟用户
guest_username=virtual              #虚拟用户映射的本地用户，即用此用户的家目录作虚拟用户的家目录
user_config_dir=/etc/vsftpd/config  #虚拟用户配置文件目录
virtual_use_local_privs=YES/NO(NO)  #为YES时，虚拟用户和本地用户有相同权限，为NO时，虚拟用户和匿名用户有相同权限

accept_timeout=60               #建立ftp连接超时时间(单位秒)
connect_time=60                 #PORT方式下建立数据连接的超时时间
data_connection_timeout=120     #建立FTP数据连接超时时间
idle_session_timeout=300        #设置session超时时间，即多长时间不对ftp服务器进行任何操作，断开连接

xferlog_enable=YES/NO(YES)          #上传下载日志记录
xferlog_file=/var/log/vsftpd.log    #日志文件名和路径
xferlog_std_format=YES/NO(NO)       #设置日志格式
log_ftp_protocol=YES/NO(NO)         #开启此选项，所有的ftp请求都会被记录，且xferlog_std_format配置不生效

listen_port=21                  #监听端口
connect_from_port_20=YES/NO     #指定20为数据传输端口
ftp_data_port=20                #PORT方式下，ftp数据连接端口
pasv_enable=YES                 #被动模式
pasv_address=0.0.0.0            #多块网卡时候，设置此参数，绑定外网网卡
pasv_min_port=40000             #被动模式的端口最小值
pasv_max_port=50000             #被动模式的端口最大值

listen=YES/NO(YES)              #是否以 standalone 模式运行，设置为NO时，vsftpd会收到xinetd服务的掌控，功能会受到限制
max_clients=0                   #最大连接数，默认0不受限制，(standalone模式有效)
max_per_ip=0                    #每个ip与ftp服务器建立的连接数，(standalone模式有效)
listen_address=0.0.0.0          #指定监听ip，(standalone模式有效)
setproctitle_enable=YES/NO(NO)  #设置每个与ftp服务器的连接，是否显示为不同的进程，(为NO 时，ps aux | grep ftp 只显示一个进程。为YES时，每个连接都有一个vsftpd进程)

ssl_enable=YES                      #开启ssl
ssl_tlsv1=YES                       #支持得ssl版本
ssl_sslv2=YES                       
ssl_sslv3=YES                       
rsa_cert_file=.../vsftpd.crt        #签发证书路径
rsa_private_key_file=.../vsftpd.key #密钥文件路径
allow_anon_ssl=YES                  #开启匿名用户(虚拟用户)ssl
force_anon_logins_ssl=YES           #强制匿名用户(虚拟用户)通过ssl登陆
force_anon_data_ssl=YES             #强制匿名用户(虚拟用户)通过ssl进行数据传输
force_local_logins_ssl=YES          #强制本地用户通过ssl登陆
force_local_data_ssl=YES            #强制本地用户通过ssl进行数据传输

```


## 命令


```sh
#指定ip和端口
ftp -n -p 192.168.1.123 12345
ftp> user
(username) 输入用户名
331 User haigui OK. Password required
Password: 输入密码
ftp>
```


## 其他

#### 匿名用户上传下载
匿名用户登陆ftp后，相当于other权限，例如用ftp用户登陆，文件所有者和所有者都是ftp，但是此登陆的用户还是用的ohter的权限

设置匿名用户上传
1. anonymous_enable=YES
2. anon_upload_enable=YES
3. 上传的目录需要有 other 的 r 权限


设置匿名用户下载
1. anonymous_enable=YES
2. 下载的文件有other的w权限(可设置anon_umask)

#### 本地用户限制主目录

本地用户登陆ftp后是否能够切换到其他目录由 chroot_local_user 和 chroot_list_enable 两个配置决定

1. 当 chroot_local_user=YES ，chroot_list_enable=NO。所有用户都不能切换到其他目录
2. 当 chroot_local_user=YES ，chroot_list_enable=YES。/etc/vsftpd/chroot_list文件中的用户可以切换其他目录，
3. 当 chroot_local_user=NO ，chroot_list_enable=YES。/etc/vsftpd/chroot_list文件中的用户不能切换其他目录，
4. 当 chroot_local_user=NO ，chroot_list_enable=NO。所有用户都能切换到其他目录


#### 本地用户仅能登陆ftp

ftp会查询登陆用户的登陆shell，并且查询是否在 /etc/shells 中

1. /etc/passwd 下设置为 /sbin/nologin
2. /etc/shells 添加一行 /sbin/nologin


#### 访问权限

1. selinux
2. tcp_wrappers
3. ftpusers
4. userlist

ftpusers 和 userlist 两个文件决定哪个用户能够访问
ftpusers 优先级高于 userlist ，即存在于 ftpusers 中的用户无论如何都访问不了ftp

1. userlist_enable=NO , user_list文件不生效，即不限制用户访问，除却ftpusers文件中的用户
2. userlist_enable=YES, userlist_deny=YES,user_list文件中的用户不能访问
3. userlist_enable=YES, userlist_deny=NO ,只有user_list文件中的用户才能访问，除却ftpusers文件中



#### 设置虚拟用户

1. 创建虚拟用户数据文件,(奇数行用户，偶数行密码)
例如创建一个vsftp.user 文件，添加好用户密码后，通过db_load 转化为 vsftp.db 文件，并且修改权限为600
```sh
db_load -T -t hash -f vsftp.user vsftp.db
chmod 600 vsftp.db
```
2. 修改 /etc/pam.d/vsftpd (文件名在vsftpd.conf中设置) 
清空原有内容，添加两行
```sh
#db=上面创建的虚拟用户的用户名密码文件
auth       required	pam_userdb.so db=/etc/vsftpd/vsftp
account    required	pam_userdb.so db=/etc/vsftpd/vsftp
```
3. 修改 vsftpd.conf ，guest_username 配置指定虚拟用户的家目录， 设置此用户的家目录的 o+r 权限
```sh
chmod o+r /home/virtual
```
4. 创建虚拟用户各自的配置文件，user_config_dir 参数指定的目录下，文件名和用户名一致
5. 虚拟用户用的配置参数和匿名用户参数一致，即 vsftpd.conf + 自己的配置文件 中匿名用户的参数配置项(可以将主配置文件中的匿名用户相关配置注释，在虚拟用户自己的配置文件中单独设置)



## vsftpvsd + openssl

openssl生成得3种密钥证书
```
*.key --> 私钥 
*.csr --> 公钥(证书)
*.crt --> 签发后得证书
```

1. 查看是否安装openssl rpm -qa | grep openssl
2. 查看vsftod是否厉害openssl库，先查看vsftpd命名所在目录
   1.  which vsftpd
   2.  ldd /usr/sbin/vsftpd | grep libssl
3. 生成密钥，证书，签发证书
   1. 生成密钥文件 openssl genrsa -out vsftpd.key 2048
   2. 生成证书文件 openssl req -new -key vsftpd.key -out vsftpd.csr
   3. 生成自签发证书 openssl x509 -req -days 365 -sha256 -in vsftpd.csr -signkey vsftpd.key -out vsftpd.crt
4. 修改vsftpd.conf，添加ssl配置相关参数
5. 重启vsftpd
