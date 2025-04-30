## sqlcmd

导入 Microsoft 存储库密钥
```sh
rpm --import https://packages.microsoft.com/keys/microsoft.asc
```

下载存储库配置文件
```sh
curl -o /etc/yum.repos.d/mssql-release.repo https://packages.microsoft.com/config/rhel/7/prod.repo
```


安装工具包
```sh
sudo yum remove unixODBC-utf16 unixODBC-utf16-devel
sudo ACCEPT_EULA=Y yum install -y msodbcsql17
sudo ACCEPT_EULA=Y yum install -y mssql-tools
sudo yum install -y unixODBC-devel
```

配置环境变量
```sh
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
```
