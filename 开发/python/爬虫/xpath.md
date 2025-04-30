# xpath

解析html页面

1. 解析本地文件
2. 解析爬取的网页
```py
from lxml import etree

# 获取本地文件对象
tree = etree.parse('a.html')

# 获取网页内容对象
content = response.read().decode('utf-8')
tree = etree.HTML(content)
```

#### xpath()用法
xpath()方法返回的是列表list
```py
# 获取ul标签下的li标签，
tree.xpath('/ul/li/')
# 获取所有li标签，// 表示子标签和子子标签
tree.xpath('//ul/li/')
tree.xpath('//li/')

# 获取标签 li的内容
tree.xpath('//li/text()')

# 获取li标签的id
tree.xpath('//ul/li[@id]')
# 获取id=a的li标签的内容
tree.xpath('//ul/li[@id="a"]/text()')

# 获取li标签的class和value
tree.xpath('//ul/li/@class')
tree.xpath('//ul/li/@value')

# 获取id为c开头的li标签
tree.xpath('//ul/li[contains(@id,"c")]')

# 获取id=a 并且 class=b 的li标签的内容
tree.xpath('//ul/li[@id="a" and @class="b"]/text()')
# 获取 id=a 或者 class=a 的li标签的内容
tree.xpath('//ul/li[@id="a"]/text() | //ul/li[@class="a"]/text()')
```

##### 不等于、不包含
```py
# div的id不等于a
tree.xpath('//div[@id!="a"]')
# div的id等于a并且class不等于haha
tree.xpath('//div[@id="a" and not[@class=haha]')
# div的id等于a并且class不包含haha
tree.xpath('//div[@id="a" and not[contains(@class,"haha")]')
```