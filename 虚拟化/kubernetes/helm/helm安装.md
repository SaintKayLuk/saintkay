# 安装helm


## 通过二进制文件安装

根据版本下载 二进制文件，下载地址 https://github.com/helm/helm/releases

```sh
curl -O https://get.helm.sh/helm-v3.13.3-linux-amd64.tar.gz
tar -zxvf helm-v3.13.3-linux-amd64.tar.gz
mv linux-amd64/helm /usr/local/bin
```


## 通过 官方脚本安装

只能安装最新版本 [get-helm-3.sh](./get-helm-3.sh)

```sh
curl -fsSL -o get-helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get-helm.sh
./get_helm.sh

# 或者一条命令直接执行

curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```



## 通过包安装

使用Apt (Debian/Ubuntu)
```sh
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] http://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
```

查询一下可安装的版本
```sh
apt-cache madison helm
```

安装指定版本
```sh
apt install helm=3.12.3-1
```