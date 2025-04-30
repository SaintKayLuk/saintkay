1. 安装 subinacl
2. 将subinacl.exe复制到system32中，方便使用CMD命令(可选)
3. 管理员方式CMD subinacl /service 服务名 /grant=[域名/]用户名=[访问权限]

* F：完全控制
* R：一般性读
* W：一般性写
* X：一般性执行
* L：读取控制
* Q：查询服务配置
* S：查询服务状态
* E：枚举从属服务
* C：提供配置更改
* T：启动服务
* O：停止服务
* P：暂停/继续服务
* I：询问服务
* U：提供用户定义的控制命令


例：给 xiaoshan 用户赋予 myService 服务的 启动、停止、暂停 权限
```
subinacl /service myService /grant=xiaoshan=top
```

