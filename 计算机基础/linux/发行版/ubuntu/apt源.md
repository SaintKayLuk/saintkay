
示例
```sh
deb http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse

# 第一部分
#   deb      二进制包
#   deb-src  源码包
# 第二部分  url，也就是软件源的地址
# 第三部分  发行版本，可以有不同的选项，例如 jammy 代表 ubuntu22.04 原始发布的软件包
#   jammy             原始发布版本的软件包
#   jammy-updates     正式发布后更新的软件包（功能更新、bug 修复）
#   ammy-backports    回移的新版软件包（主要用于非默认版本软件）
#   jammy-security    安全更新包
# 第四部分：组件
#   main        Ubuntu 官方支持的软件，完全自由
#   restricted  官方支持，但受限的驱动/软件（闭源）
#   universe    社区维护的软件包
#   multiverse  受版权或法律限制的软件包
```

22.04 的示例
```sh
deb http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ jammy-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse

# 源码包，可选
deb-src http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse
```