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

# shell文件格式
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
[root@localhost ~] echo -e "\e[1; 31m abc \e[0m"
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
修改之后需要重新加载配置文件，让其生效
~~~
[root@localhost ~]# source /etc/profile
[root@localhost ~]# . /etc/profile
~~~

source命令和 . 作用一致

在linux中 . 的作用
* 作用同source一致，重新加载配置文件
* ./ 代表当前目录
* .文件名，文件名前面加一个点，代表隐藏文件


调用历史命令

1. 使用上下箭头查看历史命令
2. 使用 !n 来执行第n条历史命令
3. 使用 !! 来执行上一条命令
4. 使用 !字符 来执行最后一条以该字符开头的命令 
5. 使用 !$ 执行上一条命令的最后一个参数

## 别名

~~~
alias 别名='原命令'

例：
alias vi='vim'
~~~

通过alias命令设置的别名是临时生效，永久生效写入 ~/.bashrc 文件中

### 命令执行的顺序

1. 绝对路径或相对路径执行的命令，例如 /bin/vi 就是执行的vi命令
2. 别名
3. 执行bash的内部命令
4. 按照 $PATH 环境变量定义的目录查找顺序找到的第一个命令


## bash常用快捷键

| 快捷键 | 作用                             |
|--------|--------------------------------|
| ctrl+A | 光标移动到命令行开头             |
| ctrl+E | 光标移动到命令行结尾             |
| ctrl+C | 强制终止当前命令                 |
| ctrl+L | 清屏，相当于clear命令             |
| ctrl+U | 删除或剪切光标之前的内容         |
| ctrl+K | 删除或剪切光标之后的内容         |
| ctrl+Y | 粘贴 ctrl+U 或 ctrl+K 剪切的内容 |


## 输入输出重定向


|设备|设备文件名|文件描述符|类型|
|-|-|-|-|
|键盘  |/dev/stdin |0|标准输入|
|显示器|/dev/stdout|1|标准输出|
|显示器|/dev/stderr|2|标准错误输出|


### 输出重定向
~~~sh
>       #覆盖
>>      #追加
~~~
标准输出重定向，>后面有空格
~~~sh
命令 > 文件
命令 >> 文件
~~~
标准错误输出重定向，>后面没有空格
~~~sh
错误命令 2>文件
错误命令 2>>文件
~~~
正确输出和错误输出同时保存
~~~sh
命令 > 文件 2>&1        
命令 >> 文件 2>&1       
命令 &>文件             
命令 &>>文件                
命令>>文件1 2>>文件2        正确输出追加到文件1，错误输出追加到文件2
~~~
### 输入重定向
~~~
wc [选项] [文件名]
    -c  统计字节数
    -w  统计单词数
    -l  统计行数
~~~


## 多命令顺序执行


~~~
:       命令1 : 命令2           多个命令按顺序执行，命令之间没有逻辑关系
&&      命令1 && 命令2          当命令1正确执行，命令2才会执行
||      命令1 || 命令2          当命令1执行不正确，则命令2才会执行，当命令1正确执行，命令2不会执行
~~~


## bash中特殊符号


### 通配符
用于匹配文件名，完全匹配，find 命令搜索文件命名中可以使用通配符
~~~
?   匹配一个任意字符
*   匹配0个或多个任意字符，也可以匹配任意内容
[]  匹配中括号中任意一个字符，[abc] 代表匹配a,b,c其中一个，一个中括号代表匹配一个字符
    [-]中间加 - ，例如[a-z],代表一个小写字母
    [^] 取反，例如[^0-9],代表匹配一个不是数字的字符
~~~

### 正则表达式
用于匹配字符串，包含匹配，grep 搜索文件中内容使用正则

~~~
?   匹配前一个字符重复0次或1次          --只能用egrep命令来使用
*   匹配前一个字符重复0次或任意多次
[]  匹配中括号中任意一个字符，[abc] 代表匹配a,b,c其中一个，一个中括号代表匹配一个字符
    [-]中间加 - ，例如[a-z],代表一个小写字母
    [^] 取反，例如[^0-9],代表匹配一个不是数字的字符
^   匹配行首
$   匹配行尾
~~~










#### read

位置参数变量使用比较不友好， read可以提示输入

~~~
read [选项] [变量名]
    -p "提示信息"   在等待read输入时，输出提示信息
    -t 秒数         read命令会一直等待用户输入，此选项选择等待秒数，等待时间内用户没有输入，会结束脚本
    -n 字符数       允许输入的最大字符数，达到指定字符数会自动回车
    -s              隐藏输入的数据，类似于登陆时输入密码
~~~

例：通过read提示用户输入，允许最大输入字符数为2，并且等待输入30秒
```sh
[root@localhost ~]# cat test.sh
#!/bin/bash
read -t 30 -n 3 -p "请输入姓名：" name 
echo $name  

[root@localhost ~]# ./test.sh
请输入姓名：sk
sk
```

## 数值运算

### 数值运算方法

#### 使用declare声明变量类型
因为shell默认变量为字符串类型，我们在做数值运算的时候可以使用declare声明变量类型为数值
```sh
declare [+/-] [选项] 变量名
    -   给变量设定类型属性
    +   取消变量的类型属性
        a   将变量声明为数组
        i   将变量声明为整数
        r   将变量声明为只读属性，一旦设置为只读属性，此变量不能改变值，也不能被删除，更不能通过 +r 取消只读属性，此声明是通过命令是临时生效的，重启失效
        x   将变量声明为环境变量
        p   显示指定的被声明的类型
```
**-是设定属性，+是取消属性**
-x 声明的环境变量，和 export 命令作用是一样，export 命令其实就是通过 declare -x 来设定为环境变量,
~~~
[user@localhost ~]$ declare -x age=18
~~~

例：通过给c设置属性为整数型，会把a+b作为数值运算
```sh
[user@localhost ~]$ a=11
[user@localhost ~]$ b=22
[user@localhost ~]$ declare -i c=$a+$b
[user@localhost ~]$ echo c
33
```

例：声明数组类型,通过 ${数组名[*]} 获取数组中所有值
```sh
[user@localhost ~]$ declare -a name[0]="pa"
[user@localhost ~]$ name[1]="spe"
[user@localhost ~]$ name[2]="jugg"
[user@localhost ~]$ echo ${name[*]}
pa spe jugg
```
通过 declare -p 来查看所有变量,也可以指定变量名来查看某个变量 declare -p 变量名
```sh
[user@localhost ~]$ declare -p
declare -- BASH="/bin/bash"
declare -r BASHOPTS="checkwinsize:cmdhist:expand_aliases:extquote:force_fignore:histappend:hostcomplete:interactive_comments:login_shell:progcomp:promptvars:sourcepath"
declare -ir BASHPID
...
```


#### 使用 expr 或 let 数值运算工具

例：使用expr进行数值运算
```
[root@localhost ~]# a=11
[root@localhost ~]# b=22
[root@localhost ~]# c=$(expr $a + $b)
[root@localhost ~]# echo $c
33
```
+号左右两侧必须要又空格

例：使用let进行数值运算
```
[root@localhost ~]# let d=$a+$b
[root@localhost ~]# echo $d
33
```

#### 使用 $(()) 或 $[] 运算

推荐使用 $(()) 方式进行数值运算

例：使用$(())进行运算
```
[root@localhost ~]# e=$(( $a+$b ))
[root@localhost ~]# echo $e
33
```
空格要求不严格，可以有空格也可以没有空格，默认都加上空格


### 运算符

|运算符|说明|
|-----|-|
|-,+  |单目负，单目正|
|!,~  |逻辑非，按位取反或补码|
|*,/,%|乘，除，取模|
|+,-  |加，减|
|<<,>>|按位左移，按位右移|
|<=,>=,<,>|小于等于，大于等于，小于，大于|
|==,!=|等于，不等于|
|$    |按位与|
|^    |按位异或|
|\|   |按位或|
|&&   |逻辑与|
|\|\| |逻辑或|
|=,+=,-=,*=,/=,%=,&=,^=,\|=,<<=,>>=|赋值，运算且赋值|

从上到下，优先级依次降低

例：加减乘除
```sh
[user@localhost ~]$ a=$(( (11+3)*3/2 ))
[user@localhost ~]$ echo $a
21
```

### 变量测试与内容置换

|变量置换方式|变量y没有设定|变量y为空值|变量y有值|
|-|-|-|-|
|x=${y-新值} |x=新值|x为空 |x=$y|
|x=${y:-新值}|x=新值|x=新值|x=$y|
|x=${y+新值} |x为空 |x=新值|x=新值|









