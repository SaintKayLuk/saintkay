
## xpath语法

| 表达式 | 藐视                          |
|--------|-----------------------------|
| /      | 从根节点开始选取              |
| //     | 不考虑层级，匹配所有符合的节点 |
| .      | 当前节点                      |
| ..     | 父节点                        |
| @      | 选取属性                      |
| *      | 匹配所有节点                  |
| @*     | 匹配所有属性                  |


选取节点
```
/a/b                从根元素开始获取a节点下的所有b节点
//a                 获取所有a元素
//a//b              获取a节点下的 所有层级的b节点
//a/text()          获取所有a标签的文本内容，即<a>这里的内容<a/>
//a[@id="abc"]      获取id为 abc 的a节点
//@abc              获取所有有 abc 属性的节点
//a/b[1]            选取a节点下的第一个b节点，索引从1开始
//a/b[last()]       a节点下的最后一个b节点
//a[@b]             获取所有有b属性的a节点
//a[@b="c"]         获取所有b属性=c的a节点
//a/@class          获取a节点的 class 值
```

选取未知节点
```
//a/*               所有a节点下的节点
//a[@*]             所有拥有属性的a节点
```

--- 

```
//a[@id="b" and @class="c"]             id=b 并且 class=c 的a节点
//a | //b                               所有a节点和b节点
//a[contains(@id,"c")]')                a节点，并且id包含c的
//div[@id!="a"]                         div的id不等于a
//div[@id="a" and not[@class="abc"]     div的id等于a并且class不等于c
//div[not(contains(@class,"abc"))]      div的class不包含abc
//div[not(@class)]                      没有class属性的div
```

#### XPath 轴

| 轴名称             | 结果                                                   |
| ------------------ | ------------------------------------------------------ |
| ancestor           | 选取当前节点的所有先辈（父、祖父等）                   |
| parent             | 选取当前节点的父节点                                   |
| child              | 选取当前节点的所有子元素。                             |
| descendant         | 选取当前节点的所有后代元素（子、孙等）                 |
| descendant-or-self | 选取当前节点的所有后代元素（子、孙等）以及当前节点本身 |
| following          | 选取当前节点之后的所有节点                             |
| following-sibling  | 选取当前节点之后的所有兄弟节点                         |
| preceding          | 选取当前节点之前的所有节点                             |
| preceding-sibling  | 选取当前节点之前的所有同级节点                         |

语法：
```
轴名称::节点[索引]

id为 kw 的input节点的所有先辈的 span标签
//input[@id=‘kw’]//ancestor::span

a标签之后的所有同级的img标签
//a/following-sibling::img
```



