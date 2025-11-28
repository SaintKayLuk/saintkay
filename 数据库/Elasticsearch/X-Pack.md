## X-Pack

X-Pack 是一个 Elastic Stack 扩展，提供安全、警报、监控、报告、机器学习和许多其他功能。默认安装



#### 内置用户创建密码

1. 修改配置文件 elasticsearch.yml

```yml
xpack.security.enabled: true
```

2. 启动elasticsearch
3. 设置密码
```sh
#自动生成密码，密码会输出到控制台
/usr/share/elasticsearch//bin/elasticsearch-setup-passwords auto
#交互方式自定义输入密码
./usr/share/elasticsearch/bin/elasticsearch-setup-passwords interactive
```
4. elasticsearch设置密码后，kibana需要密码来连接elasticsearch，修改配置文件 kibana.yml
```yml
elasticsearch.username: "kibana"
elasticsearch.password: "密码"
```
5. 启动kibana

6. 如果忘记密码，是不能再次创建密码的，需要删除  .security-7 索引，再重新生成密码
