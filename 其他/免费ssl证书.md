

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

### centos7
certbot certonly -d xxx.com --preferred-challenges dns --manual
