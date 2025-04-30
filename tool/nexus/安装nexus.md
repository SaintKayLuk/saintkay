# 安装nexus


1. 下载tar.gz 文件，解压到 /opt 目录
2. 根据下载的nexus版本，下载对应的jdk版本，解压到/opt目录，配置环境
3. 安装目录下 bin/nexus start 启动



## 配置文件

数据目录 默认为 sonatype-work 下的 etc目录

## 配置https

1. 去阿里云或者华为云等搞一个ssl证书，需要 .jks 格式
2. 放到 安装目录的 etc/ssl/ 下，改名为 keystore.jks
3. 安装目录的 etc/jetty 下，修改jetty-https.xml
```xml
<!-- 修改password，为jks的password -->
<Set name="KeyStorePassword">Je7*EaQytyTWghRy</Set>
<Set name="KeyManagerPassword">Je7*EaQytyTWghRy</Set>
<Set name="TrustStorePassword">Je7*EaQytyTWghRy</Set>
```
4. 修改配置，运行时的配置
    ```properties
    # 修改http的端口和https的端口
    application-port=80
    application-port-ssl=443
    # 取消这行注释，并且添加 ${jetty.etc}/jetty-https.xml
    nexus-args=${jetty.etc}/jetty.xml,${jetty.etc}/jetty-http.xml,${jetty.etc}/jetty-requestlog.xml,${jetty.etc}/jetty-https.xml
    ```














