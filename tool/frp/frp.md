# frp内网穿透

需要一台公网服务器，映射内网服务器

## http
公网服务器配置文件frps.toml
```
bindPort = 7000
vhostHTTPPort = 4200
```

windows启动
```
frps.exe -c ftps.toml
```

内网服务器配置文件frpc.toml
```
serverAddr = "x.x.x.x"              # 公网服务器的ip
serverPort = 7000                   # frp端口，和frps.toml配置一致

[[proxies]]
name = "web"
type = "http"
localIP = "127.0.0.1"               # 本地访问地址
localPort = 4200                    # 本地访问端口
customDomains = ["xxx.com"]         # 最终需要访问的域名
```

windows启动frpc.exe
```
frpc.exe -c frpc.toml
```


dns解析xxx.com 到公网ip，然后访问 xxx.com 即可访问内网服务器的应用