


上传 jdk.tar.gz 到 /opt 目录并解压

单个用户生效
```sh
echo 'export JAVA_HOME=/opt/jdk17.xxx' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc
```


所有用户生效
```sh
echo 'export JAVA_HOME=/opt/jdk-17' >> /etc/profile
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> /etc/profile
source /etc/profile
```