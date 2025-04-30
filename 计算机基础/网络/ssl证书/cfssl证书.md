
## 安装
```sh
wget https://github.com/cloudflare/cfssl/releases/download/v1.6.1/cfssl_1.6.1_linux_amd64
wget https://github.com/cloudflare/cfssl/releases/download/v1.6.1/cfssljson_1.6.1_linux_amd64
wget https://github.com/cloudflare/cfssl/releases/download/v1.6.1/cfssl-certinfo_1.6.1_linux_amd64
```


```sh
chmod +x cfssl*
```

```sh
mv cfssl_1.6.1_linux_amd64 /usr/local/bin/cfssl
mv cfssl-certinfo_1.6.1_linux_amd64 /usr/local/bin/cfssl-certinfo
mv cfssljson_1.6.1_linux_amd64 /usr/local/bin/cfssljson
```

## 操作

```
cfssl [command]
    command
        sign             签名证书
        bundle           
        genkey           生成私钥和证书请求
        gencert          生成私钥和证书
        serve            
        version          打印版本
        selfsign         
        certinfo        
            -cert           查看证书信息(ca.pem)
            -csr            查看证书请求文件信息
            -domain         根据域名查看证书信息
        print-defaults   打印默认配置
            csr             证书请求文件
            config          配置文件
```


### 配置文件

从默认配置复制一份
```sh
cfssl print-defaults config > config.json
cfssl print-defaults csr > csr.json
```

```json
//config.json
{
    "signing": {
        "default": {
            "expiry": "168h"
        },  
        "profiles": {
            "www": {
                "expiry": "8760h",          //证书过期时间，profiles中不写此配置则使用 default 的
                "usages": [
                    "signing",              //该证书可用于签名其他证书
                    "key encipherment",     
                    "server auth"           //该 CA 对service提供的证书进行验证
                ]   
            },  
            "client": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"           //该 CA 对client提供的证书进行验证
                ]   
            }   
        }   
    }   
}
```

```json
//csr.json
{
    "CN": "example.net",
    "CA":{
        "expiry":"175200h"          //根证书有效期
        },
    "hosts": [
        "example.net",
        "www.example.net"
    ],
    "key": {
        "algo": "ecdsa",            //加密算法，建议使用rsa
        "size": 256                 //加密算法长度，建议使用2048
    },
    "names": [
        {
            "C": "US",              //国家
            "ST": "CA",             //省，州
            "L": "San Francisco"    //城市
        }
    ]
}
```


## 生成自签名根 CA 证书和私钥

```sh
cfssl gencert -initca csr.json | cfssljson -bare ca

#最后ca表示生成的文件名为ca开头
#生成3个文件
ca.csr      证书请求文件
ca-key.pem  私钥
ca.pem      证书(公钥)
```

根证书签发下级证书
```
cfssl gencert -ca ca.pem -ca-key ca-key.pem -config config.json -profile www test-csr.json | cfssljson -bare test
```

根证书有效期由 ca-csr.json 决定
其他证书有效期由 config.json 决定
