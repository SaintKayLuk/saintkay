# Kubernetes 代理



需要gitlab开启代理服务器，社区版默认启用代理服务器
```rb
# gitlab_kas['enable'] = true
```



本地 gitlab 集群 要访问 云上 k8s 集群 ，通过在 k8s 里安装代理


代理需要访问本地的集群设置，可以通过nat， 如果 nat不能转发 443 端口

则 域名解析到本地 比如 gitlab.wecharmer.com  --> 192.168.4.75

https://gitlab.wecharmer.com  本地访问 192.168.4.75

在路由器上设置 ddns， nat映射443 到外网4433 ，然后 再加一个域名 例如 gitlab-agent.wecharmer.com 指向 ddns 的域名 xxx.com


在gitlab上 的 https 证书要用 通配符 *.wecharmer.com 的证书

然后最后 注册的 agent 的 wss地址 要改为 gitlab-agent.wecharmer.com 的地址 例如  wss://gitlab-agent.wecharmer.com:4433/-/kubernetes-agent/

