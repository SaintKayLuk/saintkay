# jsonpath

解析json文件

jsonpath语法
```
$   相当于根标签
.   相当于下一级
..  相当于子集和所有子集

```

```py
import json
import jsonpath

# 导入本地json文件
obj = json.load(open('text.json', 'r', encoding='utf-8'))

# 导入response返回
...
content = response.read().decode('utf-8')
obj = json.loads(content)


# 例：查询a键下所有b键下的c
jsonpath.jsonpath(obj, '$.a.b[*].c')

# 例：查询所有a键的值
jsonpath.jsonpath(obj, '$..a')

# 例：查询a键下的所有内容
jsonpath.jsonpath(obj, '$.a.*')

# 例：查询a下的所有b的值，包括子集合所有子集
jsonpath.jsonpath(obj, '$.a..b')

# 例：查询所有a键的第三个值
jsonpath.jsonpath(obj, '$..a[2]')
```



