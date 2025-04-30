

https://dev.mysql.com/downloads/mysql/


初始化mysql，会创建一个没有密码的root用户
```
mysqld --initialize-insecure
```

添加mysql到windows的服务中
```
mysqld --install
```
启动/停止 MySQL 服务：
```
net start MySQL
net stop MySQL
```

删除 mysql 服务
```
sc delete mysql
```