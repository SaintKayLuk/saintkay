## go下载地址
```
https://golang.google.cn/dl/
```

1.15.15版本


## 命令

```go
go build        //编译
go run          //直接运行 .go 文件，隐藏了编译过程
go get

```


## 注释

```go
//单行注释      

/*
多行
注释
*/    
```

## 关键字

#### package

和java一样，包名

* 必须存在，且在第一行
* 生成可执行程序必须要有 package main，且有 func main()
* 运行单个文件，必须为 package main


#### import
引入包

* 两种语法
```go
import "package1"
import "package2"
import "package3"


import {
    "package1"
    "package2"
    "package3"
}
```
* 导入依赖的package包
* 不能导入没有用到的package包，会报错
* 按顺序导入，并初始化导入包的常量变量等，并执行init()函数
* 多次导入只会被导入一次，即init()函数只能被执行一次
* 起别名，以别名来调用(以abc代替package1包命来调用)
```go
import abc "package1"
```
* 点 . 来标识，执行该包中的方法省略包名
```go
import . "package1"
```
* 下划线 _ 标识，不导入整个包，只执行包中的init()函数
```go
import _ "package1"
```










## 转义

```go
package main
import "fmt"
func main(){
    fmt.Println("aaa\tbbb")//制表符
	fmt.Println("aaa\nbbb")//换行
	fmt.Println("aaa\\bbb")//输出一个\
	fmt.Println("aaa\"bbb")//输出一个"
	fmt.Println("aaa\rbbb")//回车。相当于 \r后面的会替换前面相同字符内容
}

```


## public/private

方法，函数，变量名第一个字母大写代表 public，其他包也能用，第一个字母小写，相当于private只能自己使用



