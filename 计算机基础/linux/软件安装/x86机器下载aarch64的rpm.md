

创建一个新的仓库
```sh
sudo vi /etc/yum.repos.d/aarch64.repo
```

添加如下内容
```
[aarch64-base]
name=CentOS-7 - Base - aarch64
baseurl=http://vault.centos.org/altarch/7/os/aarch64/
enabled=1
gpgcheck=0

[aarch64-updates]
name=CentOS-7 - Updates - aarch64
baseurl=http://vault.centos.org/altarch/7/updates/aarch64/
enabled=1
gpgcheck=0

[aarch64-extras]
name=CentOS-7 - Extras - aarch64
baseurl=http://vault.centos.org/altarch/7/extras/aarch64/
enabled=1
gpgcheck=0

[aarch64-epel]
name=Extra Packages for Enterprise Linux 7 - aarch64
baseurl=http://mirror.us.leaseweb.net/epel/7/aarch64/
enabled=1
gpgcheck=0
```


在联网的 x86 机器上下载 aarch64 架构的软件包及其依赖项
由于直接使用 yumdownloader 下载 aarch64 包会导致依赖冲突，所以使用 reposync 来同步整个存储库，然后手动选择所需的包
```sh
# 同步基础存储库
reposync -r aarch64-base --arch=aarch64 --download-metadata

# 同步更新存储库
reposync -r aarch64-updates --arch=aarch64 --download-metadata

# 同步额外存储库
reposync -r aarch64-extras --arch=aarch64 --download-metadata

# 同步 EPEL 存储库
reposync -r aarch64-epel --arch=aarch64 --download-metadata
```

打包整个仓库
```sh
tar -czvf centos7-aarch64-repo.tar.gz  aarch64-base
```

目标机器上
```sh
mkdir -p /mnt/centos7-aarch64-repo
tar -xzvf /path/to/destination/centos7-aarch64-repo.tar.gz -C /mnt/centos7-aarch64-repo
```

```sh
cat <<EOF > /etc/yum.repos.d/local-aarch64.repo
[local-aarch64-base]
name=Local CentOS-7 - Base - aarch64
baseurl=file:///mnt/centos7-aarch64-repo/aarch64-base
enabled=1
gpgcheck=0

[local-aarch64-updates]
name=Local CentOS-7 - Updates - aarch64
baseurl=file:///mnt/centos7-aarch64-repo/aarch64-updates
enabled=1
gpgcheck=0

[local-aarch64-extras]
name=Local CentOS-7 - Extras - aarch64
baseurl=file:///mnt/centos7-aarch64-repo/aarch64-extras
enabled=1
gpgcheck=0

[local-aarch64-epel]
name=Local Extra Packages for Enterprise Linux 7 - aarch64
baseurl=file:///mnt/centos7-aarch64-repo/aarch64-epel
enabled=1
gpgcheck=0
EOF
```


安装
```sh
sudo yum clean all
#通过 --disablerepo="*" 和 --enablerepo=local-aarch64-* 确保只使用本地存储库。
sudo yum install gcc make --disablerepo="*" --enablerepo=local-aarch64-*
```
