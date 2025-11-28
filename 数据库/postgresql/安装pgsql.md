## 使用包安装


yum安装
```sh
#添加源
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

#安装制定版本
sudo yum install -y postgresql14-server

#初始化数据库
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb

#设置开机自启
sudo systemctl enable postgresql-14

#启动
sudo systemctl start postgresql-14
```


#### ubuntu 安装


自动配置仓库
```sh
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh

# 修改一下 /etc/apt/sources.list.d/pgdg.list 把 http 源改为 https
sed -i 's/http:/https:/g' /etc/apt/sources.list.d/pgdg.list

sudo apt update
```


安装指定版本，例如安装 15 版本
```sh
sudo apt install postgresql-15 postgresql-client-15 -y
```


### 安装完目录结构

可执行目录
```
/usr/pgsql-14
    /bin
        psql

    /lib
    /share
```


数据目录
```sh
/var/lib/postgresql
```


配置文件
```sh
/etc/postgresql
```



## 安装后设置

```sh
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb
```

默认用户为 postgres ，并且没有密码

切换为postgres
```sh
sudo -i -u postgres
```

登录postgresql
```sh
psql
```

设置个密码
```sh
ALTER USER postgres WITH PASSWORD '你的新密码';
```

退出 pgsql
```sh
\q
```