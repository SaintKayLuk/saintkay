## 安装nginx


```sh
#安装依赖
yum -y install wget gcc gcc-c++ openssl openssl-devel pcre-devel zlib zlib-devel

#下载源码包
wget http://nginx.org/download/nginx-1.16.1.tar.gz                 
#解压源码包
tar -zxvf nginx-1.16.1.tar.gz
#进入解压目录    
cd nginx-1.16.1
```


编译前准备       
1. 在安装前检测系统环境是否符合要求
2. 定义需要的功能选项，一般使用 ./configure --prefix=安装路径 来指定安装路径
3. 把系统环境的检测结果和定义好的功能写入Makefile文件，后续编译和安装需要依赖这个文件 
```sh
./configure
	--prefix=path					
	--with-http_ssl_module				
	--with-http_stub_status_module		


	--add-module=/第三方模块目录

#自定义nginx安装目录，默认为 /usr/local/nginx
--prefix=path	
#添加ssl模块，可开启https的监听
--with-http_ssl_module
#性能统计模块
--with-http_stub_status_module
```

编译，调用gcc编译器，并读取Makefile文件中的信息
```sh                  
make

#(可选命令)，清空 ./configura 和 make 命令产生的内容  (在安装出错的情况下，可用此命令，并重新编译)               
make clean                 
#安装，会将编译完的nginx安装到--prefix=path 的路径下
make install
```


## 安装过程中可能出现的问题


```
./configure: error: the HTTP rewrite module requires the PCRE library.
You can either disable the module by using --without-http_rewrite_module
option, or install the PCRE library into the system, or build the PCRE library
statically from the source with nginx by using --with-pcre=<path> option.

#HTTP重写模块需要PCRE库，禁用 -without-http_rewrite_module option 或者安装一下pcre库
yum -y install pcre-devel
```


```
./configure: error: the HTTP gzip module requires the zlib library.
You can either disable the module by using --without-http_gzip_module
option, or install the zlib library into the system, or build the zlib library
statically from the source with nginx by using --with-zlib=<path> option.

#缺少gzip库
yum install -y zlib-devel
```


## 添加模块

例如源码解压包在 /root/nginx-1.6.1/，在/root/nginx-1.6.1/路径下执行 ./configure --prefix=/opt/nginx 时候，最后的程序在 /opt/nginx
添加模块需要再次编译nginx，即在 /root/nginx-1.6.1/ 下操作 

查看已安装模块
```
nginx -V
```

例如添加 ssl模块
```sh
./configure --prefix=/opt/nginx --with-http_ssl_module
#编译
make

#make install会覆盖原来的/opt/nginx 文件夹,所以不能make install
#make install 
```

备份原来的nginx
```
mv /opt/nginx/sbin/nginx /opt/nginx/sbin/nginx.bak
```

把当前目录下的 objs/nginx 移动到原nginx目录
```
mv ./objs/nginx /opt/nginx/sbin/nginx
```

重启nginx
```
nginx -s stop
nginx
```

### 添加xxx模块
git clone git://github.com/yaoweibin/ngx_http_substitutions_filter_module.git
	--add-module=/第三方模块目录

--with-http_sub_module --add-module=路径/ngx_http_substitutions_filter_module/
## 升级