# 免费ssl证书

## certbot

### centos6

certbot-auto certonly --webroot --webroot-path /usr/local/java/nginx/html -d yintai.xclearn.com

certbot-auto certonly --webroot --webroot-path /usr/local/java/nginx/html -d map.yintaijiaoyu.cn

certbot-auto certonly --no-self-upgrade --webroot --webroot-path /usr/local/java/nginx/html -d map.gbc-edu.cn

更新
~~~
certbot-auto renew --no-self-upgrade  --force-renew
--force-renew       强制更新
--no-self-upgrade   不升级certbot-auto，不添加此参数会自动升级到最新版本
~~~

查看证书
~~~
certbot-auto certificates
~~~



### centos7 & ubuntu

```
certbot
    --register-unsafely-without-email
```



```sh
certbot certonly -d xxx.com --preferred-challenges dns --manual

#查看证书
certbot certificates
#更新证书
certbot renew       #更新所有证书
    --force-renew   #强制更新

#删除证书域名为xxx.com的证书
certbot delete --cert-name xxx.com
```

续订某一个证书
```sh
certbot certonly --force-renewal -d *.xxx.com --standalone
```