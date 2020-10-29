

## certbot

### centos6
certbot-auto certonly --email rapzogo@snapmail.cc -d xxx.com --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory --no-self-upgrade


certbot-auto certonly --webroot --webroot-path /usr/share/nginx/html --email rapzogo@snapmail.cc -d xxx.com 

certbot-auto certonly --webroot --webroot-path /usr/local/java/nginx/html -d yintai.xclearn.com


certbot-auto certonly --webroot --webroot-path /usr/local/java/nginx/html -d map.yintaijiaoyu.cn

certbot-auto certonly --webroot --webroot-path /usr/local/java/nginx/html -d biyoushijiaoyu.cn

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
