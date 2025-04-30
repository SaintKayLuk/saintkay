## 启用https

修改 gitlab.rb 文件，external_url 的地址需要加上https

```rb
external_url https://gitlab.example.com
```


### 启用 Let’s Encrypt 集成

需要服务器能在互联网访问

### 手动配置证书


修改配置文件
```rb
external_url https://gitlab.example.com
letsencrypt['enable'] = false
```

手动使用 Let’s Encrypt 生成证书后

将证书和私钥放到 ssl目录下，命令需要 域名.key  和 域名.crt
```sh
mkdir -p /etc/gitlab/ssl

# gitlab.example.com.key 对应 Let's Encrypt 生成的 privkey.pem
cp gitlab.example.com.key /etc/gitlab/ssl/

# gitlab.example.com.crt 对应 Let's Encrypt 生成的 fullchain.pem
cp gitlab.example.com.crt /etc/gitlab/ssl/
```

再把证书文件 域名.crt 放到 /etc/gitlab/trusted-certs 目录下




重新配置gitlab
```sh
gitlab-ctl reconfigure
```



#### 升级证书

将更新的 .key 和 .crt 文件放在 /etc/gitlab/ssl 下，替换原来的两个文件

再将 .crt 文件替换 /etc/gitlab/trusted-certs 下的文件

最后重启 nginx 模块

```sh
gitlab-ctl restart nginx
```