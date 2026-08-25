## Install with Debian package

文档地址：https://www.elastic.co/guide/en/kibana/7.17/deb.html

安装目录为：/usr/share/kibana
配置目录为：/etc/kibana


导入公钥
```sh
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
```

直接安装
```sh
sudo apt-get install apt-transport-https
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list

sudo apt-get update && sudo apt-get install kibana
```



内网环境或者网络不好的情况下直接下载 deb 包
```sh
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.17.29-amd64.deb
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.17.29-amd64.deb.sha512
shasum -a 512 kibana-7.17.29-amd64.deb 
sudo dpkg -i kibana-7.17.29-amd64.deb
```









