# markdown
Markdown 是一种轻量级标记语言，它允许人们使用易读易写的纯文本格式编写文档。
Markdown 语言在 2004 由约翰·格鲁伯（英语：John Gruber）创建。
Markdown 编写的文档可以导出 HTML 、Word、图像、PDF、Epub 等多种格式的文档。
Markdown 编写的文档后缀为 .md 或 .markdown

## markdown标题

使用 **#** 号可表示 1-6 级标题，一级标题对应一个 **#** 号，二级标题对应两个 **#** 号，以此类推。

~~~
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
~~~


## markdown段落

Markdown 段落没有特殊的格式，直接编写文字就好

### 字体

~~~
*斜体文本*
_斜体文本_
**粗体文本**
__粗体文本__
***粗斜体文本***
___粗斜体文本___
~~~

### 分割线

你可以在一行中用三个以上的星号、减号、底线来建立一个分隔线，行内不能有其他东西。你也可以在星号或是减号中间插入空格。下面每种写法都可以建立分隔线：

~~~
***
* * *
*****
---
-----
~~~

## markdown列表

### 无序列表 

无序列表使用星号(*****)、加号(**+**)作为列表标记：

~~~
* 第一行
* 第二行
* 第三行

+ 第一行
+ 第二行
+ 第三行

~~~

### 有序列表

有序列表使用数字并加上 **.** 号来表示

~~~
1. 第一行
2. 第二行
3. 第三行
~~~

### 列表嵌套

## markdown区块
## markdown代码

~~~
用 ` 代码 ` 包裹代码

也可以用 


 '~~~'
 
 

~~~

## markdown链接或跳转

**链接**
~~~
[链接名称](链接地址)
或者
<链接地址>
~~~

**页面内跳转**
~~~
[文字](#锚点)

<div id="锚点">内容</div>
<span id="锚点">内容</span>
~~~

## markdown图片

### 插入本地图片

可用相对路径或者绝对路径

```
![alt 属性文本](本地图片地址)
![alt 属性文本](本地图片地址 "可选标题")
```

### 插入网络图片

~~~
![alt 属性文本](网络图片地址)
![alt 属性文本](网络图片地址 "可选标题")
~~~

### 图片存入markdown文件

~~~
![alt 属性文字](图片base64)
~~~

base64会很长，很占地方，我们可以在文件底部

~~~
[自定义图片名]:图片base64
再调用 ![][自定义图片么]
~~~



## markdown表格
~~~
|标题1|标题2|
|--|--|
|第一行内容1|第一行内容2|
|第二行内容1|第二行内容2|
~~~
|标题1|标题2|
|--|--|
|第一行内容1|第一行内容2|
|第二行内容1|第二行内容2|



