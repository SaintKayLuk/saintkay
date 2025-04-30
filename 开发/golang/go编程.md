## 命名规则

* 大小写字母，数字和下划线
* 不能以数字开头
* 不能是关键字

## 定义变量

```go
var a int = 10
var b int
var c = 10
//声明变量并赋值
d := 10
//声明多个布尔类型变量
var vname1, vname2, vname3 bool
```


## 定义常量

使用 const 关键字定义常量

```go
const a = "hello"
const a, b = 11, 22
```

iota：特殊常量，const每出现一次，则iota加一


## 字符串拼接

用 + 拼接字符串，也可以使用 , 但是使用逗号会有空格

```go
import "fmt"
func main(){
    fmt.Println("aaa"+"bbb")
    fmt.Println("aaa","bbb")
}
  ↓
go run 
  ↓
aaabbb
aaa bbb
```


## 运算符

#### 算术运算符
| 运算符 | 描述 |
|--------|-----|
| +      | 加   |
| -      | 减   |
| *      | 乘   |
| /      | 除   |
| %      | 求余 |
| ++     | 自增 |
| --     | 自减 |

#### 关系运算符
| 运算符 | 描述                                          |
|--------|---------------------------------------------|
| ==     | 判断两个值是否相等，相等返回ture，否则返回false |
| !=     | 判断两个值是否不相等                          |
| >      | 判断左边值是否大于右边                        |
| <      | 判断左边值是否小于右边                        |
| >=     | 判断左边值是否大于等于右边                    |
| <=     | 判断左边值是否小于等于右边                    |

#### 逻辑运算符

| 运算符 | 描述                            |
|--------|-------------------------------|
| &&     | and运算符，两边都是true返回true  |
| \|\|   | or运算符，一边是true就返回ture   |
| !      | 取反运算符，如果true，则返回false |



## 条件语句

```go
a := 10
if a < 20 {
  fmt.Println("a小于20")
}else {
  fmt.Println("a大于20")
}
```

```go
var grade string = "B"
var marks int = 90

switch marks {
case 90:
  grade = "A"
case 80:
  grade = "B"
case 50, 60, 70:
  grade = "C"
default:
  grade = "D"
}
```

## 循环语句

```go
//a初始为0，少于10执行循环，每次自增
for a := 0; a < 10; a++ {
  //当a=5的时候退出循环
  if a == 5 {
    break
  }
  //当a=3的时候，跳过此次循环
  if a == 3 {
    continue
  }
  //当a=7的时候，直接跳转到breakHere方法，对于多重嵌套循环比较实用
  if a == 7 {
    goto breakHere
  }
  ...
}

breakHere:
  fmt.Println("done")
```

```go
//条件为true，无限循环
for true  {
    fmt.Printf("这是无限循环。\n");
}
```





