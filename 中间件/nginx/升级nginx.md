

#### ubuntu 22.04 通过 apt安装
```sh
mkdir -p /etc/apt/keyrings

curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo gpg --dearmor -o /etc/apt/keyrings/nginx.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/nginx.gpg] \
https://nginx.org/packages/ubuntu $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list > /dev/null

apt update
# 查看一下可安装版本
apt-cache madison nginx

# 安装1.26.0 版本
apt install nginx=1.26.0-1~jammy


```