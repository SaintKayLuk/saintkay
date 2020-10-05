
#### 生成gpg密钥
git commit需要 name 和 email，可通过一下命令查看
~~~
git config user.name
git config user.email
~~~


通过gpg 验证每次commit为本人
~~~
gpg --gen-key

根据情况填写 Real name和Email address

~~~

查看GPG密钥
~~~
gpg --list-secret-keys --keyid-format LONG <your email>

sec   rsa4096/30F2B65B9246B6CA 2017-08-18 [SC]
      D5E4F29F3275DC0CDA8FFC8730F2B65B9246B6CA
uid                   [ultimate] Mr. Robot <your_email>
ssb   rsa4096/B7ABC0813E4028C0 2017-08-18 [E]
~~~

导出该ID的公共密钥
~~~
gpg --armor --export 30F2B65B9246B6CA
~~~

#### gitlab配置
复制到gitlab gpgkey的位置



#### git配置
~~~
将密钥ID添加到git设置中
git config --global user.signingkey 831CF40177EA9999

让所有项目都启用签名验证
git config --global commit.gpgsign true
~~~