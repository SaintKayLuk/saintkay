
nginx采用异步非阻塞，I/O多路复用epoll模型



## 工作模式

* master-worker模式(默认)
* 单进程模式
  * 一般开发调试中使用，生产环境不使用




## nginx基本命令

```
nginx
	-v		查看nginx版本
	-V		查看 nginx 版本、编译器版本和配置参数。
	-t		测试配置文件是否正确
	-T		测试配置文件是否正确，并输出
	-s		向主进程发送信号
		stop		快速关闭
		quit		优雅的关闭
		reload		重新加载配置文件
```

例：
```sh
#启动nginx
nginx
#停止nginx
nginx -s stop
```


## nginx跨越设置

可以添加在server下或者location下

~~~
server{
	listen 80;
	add_header Access-Control-Allow-Origin *;
	add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
	add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';

	location / {
    	...
	}       
}
~~~

或

~~~
location /{
	add_header Access-Control-Allow-Origin *;
	add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
	add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
    ...
}
~~~


匹配不到资源文件跳转index.html
```
try_files $uri $uri/ /index.html;
```




## nginx性能统计

添加性能统计模块
```
./configure --with-http_stub_status_module	
```


在nginx.conf配置文件中添加 访问路径
```
location /status {
      stub_status on;
      access_log off;
}
```

浏览器访问 ip:port/status
```
Active connections: 2 
server accepts handled requests
 2 2 3
Reading: 0 Writing: 1 Waiting: 1 


Active connections		当前活跃连接数
server accepts			已处理连接数 
server handled 			已处理句柄，即tcp连接
server requests			已处理的请求
2 2 3 代表处理了2个连接，成功2个tcp连接，处理了3个请求

Reading			读取客户端的Header信息数.这个操作只是读取头部信息，读取完后马上进入writing状态，因此时间很短
Writing			响应数据到客户端的Header信息数.这个操作不仅读取头部，还要等待服务响应，因此时间比较长。
Waiting			开启keep-alive后等候下一次请求指令的驻留连接
```

## 密码验证

安装密码生成工具
```sh
yum install -y httpd-tools
```

```
htpasswd
	-c		创建一个密码文件
	-b		直接输入密码，而不用交互式输入密码,密码默认md5加密
```

例：创建一个密码文件 passwd 并且创建一个 test1 用户,密码为123456
```
[root@localhost ~]# htpasswd -cb /opt/nginx/conf/passwd test1 123456
Adding password for user test1
[root@localhost ~]# cat /opt/nginx/conf/passwd
test1:$apr1$RoGgiGFo$jJHJvU9aiymtTV2fIg0aU1
```

例：在passwd文件中添加一个test2帐号,不能使用-c不然会覆盖文件
```
[root@localhost ~]# htpasswd -b /opt/nginx/conf/passwd test2 123456
Adding password for user test2
[root@localhost ~]# cat /opt/nginx/conf/passwd
test1:$apr1$RoGgiGFo$jJHJvU9aiymtTV2fIg0aU1
test2:$apr1$IuAJKODT$j/4UQ4rqYKC1v.rQbLrMC/
```

修改nginx配置文件,在server下或者location下添加以下2行

```conf
#密码提示，虽然好像并没提示，但是这行必须要，不然不会提示输入密码
auth_basic "Please input password";
#密码文件位置
auth_basic_user_file /opt/nginx/conf/passwd;
```

重新加载nginx配置文件
```
[root@localhost ~]# nginx -s reload
```

## ip访问限制

允许和拒绝某个ip或者ip段的访问

修改配置文件，在server下或者location下添加allow和deny

例：允许192.168.1.15的IP能访问80端口，并且禁止192.168.1.0/24网段的ip访问，允许其他ip的访问

```conf
server {
	listen       80;
	server_name  localhost;
	allow 192.168.1.15;
	deny 192.168.1.0/24;
	location / {
		root   html;
		index  index.html index.htm;
	}
}
```

例：允许192.168.1.15能访问 80端口的 /abc 路径，并且禁止其他所有ip访问
```conf
server {
	listen       80;
	server_name  localhost;

	location /abc {
		root	html;
		index 	index.html index.htm;
		allow	192.168.1.15;
		deny	all;
	}
}
```


## 域名访问

正常情况一个端口只能对应一个server，通过域名绑定，可以实现同端口多个server

例：通过test.com访问，当存在端口为80.server_name为localhost的时候，此server只能通过test.com访问
```conf
server {
	listen       80;
	server_name  test.com;
	location / {
		root   html;
		index  index.html index.htm;
	}
}
```

## 反向代理

例：访问此server的 /abc 路径实际是访问 192.168.1.88 地址
```conf
location /abc/ {
	proxy_pass http://192.168.1.88;			#请求转发到192.168.1.88
	proxy_set_header Host $host;			#重写代理头部，保证代理访问的2级页面也能正常打开
}
```


## 负载均衡

nginx支持3种负载均衡方式
* round-robin(轮询，默认不用写)
* least_conn(最少连接)
* ip_hash

通过反向代理 proxy_pass 将请求转发到多个服务

添加upstream标签，和server同级

例：通过ip_hash的方式负载均衡到3个服务器
```conf
upstream abc {
	ip_hash;
	server srv1.example.com;
	server srv2.example.com;
	server srv3.example.com;
}

server{}
...
location /abc/ {
	proxy_pass http://abc;			#请求转发到192.168.1.88
	proxy_set_header Host $host;
}
```


例：轮询负载均衡的加权，每5个请求有3个会转发到 srv1.example.com
```
upstream abc {
	server srv1.example.com weight=3;
	server srv2.example.com;
	server srv3.example.com;
}
```
会话持久性：因为轮询和最少连接，每次不一定访问的是同一个后端服务，需要会话持久性的时候，建议使用 ip-hash 的负载均衡方式


例：备用服务，服务srv1不可用的情况下才会连接srv2
```
upstream abc {
	server srv1.example.com;
	server srv2.example.com backup;
}
```

## 使用https

添加ssl模块
```sh
./configure --with-http_ssl_module		
```

生成证书文件

```conf
# 所有访问 test.com 的80端口 转发到https
server {
	listen		80;
	server_name test.com;
	rewrite ^(.*)$	https://$host$1	permanent;
}
server {
	listen       443 ssl;
	server_name test.com;
	ssl_certificate      /etc/letsencrypt/live/test.com/fullchain.pem;
	ssl_certificate_key  /etc/letsencrypt/live/test.com/privkey.pem;
	ssl_session_cache    shared:SSL:1m;
	ssl_session_timeout  5m;
	ssl_ciphers  HIGH:!aNULL:!MD5;
	ssl_prefer_server_ciphers  on;
	location / {
		root   html;
	}
}

```