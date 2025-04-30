## Omnibus 包安装

直接安装，例如 yum install 和 apt install


```sh
sudo apt-get update
sudo apt-get install -y curl openssh-server ca-certificates tzdata perl
```

```sh
sudo apt-get install -y postfix
```

```sh
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
```

添加源和gpk

安装
```sh
GITLAB_ROOT_PASSWORD="f3cwMEjuJ7dvKC" EXTERNAL_URL="https://gitlab.wecharmer.com"  apt install gitlab-ce=16.11.8-ce.0
```

安装完的目录结构

配置文件目录
```sh
/opt/gitlab

/opt/gitlab/gitlab.rb           #主配置文件
/opt/gitlab/gitlab-secrets.json #加密文件，gitlab各组件之间的秘钥等
/opt/gitlab/ssl/                #ssl证书目录，手动设置https把证书放在此路径下，没有则手动创建
/opt/gitlab/trusted-certs/      #证书信任目录，把 gitlab.example.com.pem 文件放此路径下
```


应用程序目录
```sh
/opt/gitlab/
```


数据目录
```sh
/var/opt/gitlab/

/var/opt/gitlab/git-data/repositories   #仓库目录
/var/opt/gitlab/backups                 #备份目录
```


日志目录
```sh
/var/log/gitlab
```


## 卸载 

sudo gitlab-ctl stop && sudo gitlab-ctl remove-accounts


删除所有数据
sudo gitlab-ctl cleanse && sudo rm -r /opt/gitlab



# Debian/Ubuntu
sudo apt remove gitlab-ce

# RedHat/CentOS
sudo yum remove gitlab-ce