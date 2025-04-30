

centos7 默认使用python2.7

python指向python2.7
yum使用的是python2.7，如果需要修改默认python，则需要修改yum文件

1. 通过yum安装
    ```sh
    # 最新版本3.6，需要更高版本则编译安装
    yum install python
    ```
2. 通过源码安装
    ```sh
    wget https://www.python.org/ftp/python/3.10.11/Python-3.10.11.tgz
    ./configure --enable-optimizations
    make
    make install
    ```