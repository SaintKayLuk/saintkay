curl是一种使用支持的协议之一从服务器或向服务器传输数据的工具

```sh
curl [选项] URL

    -o file         #下载网页,并保存为file文件，也可以用重定向 curl baidu.com >> index.html
    -O              #下载网页文件，必须精确到某个文件
    -x ip:port      #设置代理
    -c file         #保存cookie信息到file文件中
    -b file         #使用cookie信息从file文件中
    -D file         #保存headers信息到file文件中
    -A "xxx"        #模拟浏览器登陆，自行填值
    -e "xxx"        #模拟 referer ，让请求从某个自定义地址跳转过来。
    -I              #只显示head内容
    -H/--header     #自定义头部信息
    -G/--get        #以get方式请求，(默认)
    -X [GET/POST/..]    #自定义请求方式，例如以POST方式请求 -X POST
    -d/--data           #post提交时数据
    -s, --silent    #静音模式，不输出任何内容
    -u username:password    #添加访问需要的用户名密码
    -k              #请求https的时候使用了自签名证书，而 curl 默认要求一个受信任的证书。可以通过-k绕过
```

例：post提交json数据
```sh
curl -X POST -H "Content-Type: application/json" -d '{"doc":{"name":"李四"}}' http://127.0.0.1:8888/test/
```

例：post提交表单数据
```sh
curl -X POST  -d "aa=123&bb=234" http://127.0.0.1:8888/test/
```