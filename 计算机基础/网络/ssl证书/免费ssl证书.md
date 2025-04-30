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
certbot renew
    --force-renew   强制更新

#删除证书域名为xxx.com的证书
certbot delete --cert-name xxx.com
```

泛域名需要DNS验证，续期的时候需要脚本去验证，如果不能实现，则再申请一次
```sh

certbot certonly -d *.gov-eye.com --preferred-challenges dns --manual

...
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: Keep the existing certificate for now
2: Renew & replace the certificate (may be subject to CA rate limits)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate number [1-2] then [enter] (press 'c' to cancel): 2
Renewing an existing certificate for *.gov-eye.com
```