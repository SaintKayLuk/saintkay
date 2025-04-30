

## CA

证书的签发机构
* 有权威的证书认证中心
* 也可以自己本地的认证中心

## PEM

证书，一般后缀为 .pem .key .crt
CA证书：CA机构颁发的证书

例：证书相当于公钥，ca.pem为证书(公钥)，ca-key.pem为私钥

## CSR

向 CA 机构申请证书用的 请求文件




## 证书链

可以通过 .csr 证书请求文件，为证书签发子证书

* 证书有效期取决于证书链中过期时间最近的

例：a证书为根证书，有效期到2022年1月1日，a签发b证书，有效期到2023年1月1日，b证书签发c证书，有效期到2024年1月1日，则c证书有效期到2022年1月1日

证书ca.pem示例：如下为c证书
```
-----BEGIN CERTIFICATE-----
c证书
-----END CERTIFICATE-----

#默认证书链
c证书 -> b证书 -> a证书
```


证书可以有不同的证书链，我们可以自定义证书链(前期是此上一级证书链签发)
```
-----BEGIN CERTIFICATE-----
c证书
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
e证书
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
a证书
-----END CERTIFICATE-----

#此c证书的证书链
c证书 -> e证书 -> a证书
```


