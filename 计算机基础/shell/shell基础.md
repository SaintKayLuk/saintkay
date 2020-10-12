# shell概述

hell是用户和Linux内核之间的接口程序，linux命令通过shell去调用内核

# shell分类

|shell类别|简称||
|-|-|-|
|Bourne      |sh  |被bash向下兼容取代
|Korn Shell  |ksh |
|Bourne Again|bash|linux默认shell
|POSIX Shell |psh |
|C Shell     |csh |被tcsh向下兼容取代
|TC Shell    |tcsh|








# shell执行方式

1. 赋予执行权限，直接运行，通过路径找到此文件
2. 通过bash调用 例：bash 文件名

shell文件格式
~~~
#!/bin/bash
...
~~~
第一行定义此文件是shell脚本文件

# bash基本功能

## echo

~~~
echo [选项] [输出内容]
    -e  支持反斜线控制的字符转换，控制字符如下
    -n  取消输出后行末的换行符(输出内容后不换行，默认一个echo输出内容后会换行)


控制字符     作用
\\          输出 \ 本身
\a          输出警告音
\b          退格键，也就是向左删除
\c          取消输出行末的换行符，和 -n 选项作用一致
\e          EXCAPE键
\f          换页符
\n          换行符
\r          回车键
\t          制表符，相当于 Tab 键
\v          垂直制表符
\0nnn       按照八进制 ASCII 码表输出字符 0 是数字0 ，nnn是三位八进制数
\xhh        按照十六进制 ASCII 码表输出字符， x 是小写字母x ，hh 是两位十六进制数

~~~

echo 输出颜色

\e[1; 代表颜色输出开始
\e[0m 代表颜色输出结束

31m 代表红色字体，32代表绿色字体等

例：输出红色的 abc 字符
~~~
echo -e "\e[1; 31m abc \e[0m"
~~~

## 历史命令

~~~
history
    -c  清空历史命令
    -w  把缓存中的历史命令写入历史命令保存文件，默认位于 ~/.bash_history
~~~

history 命令查看的历史命令是 ~./bash_history 文件中加缓存中的历史命令，默认退出登陆会把本次登陆的历史命令写入 ~/.bash_history w文件，也可以使用 history -w 来手动保存

历史命令保存条数默认1000条，在 /etc/profile 文件中修改
~~~
[root@localhost ~]# vi /etc/profile
...
HISTSIZE=1000
...
~~~




