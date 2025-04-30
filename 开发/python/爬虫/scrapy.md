# scrapy


## idea 安装 scrapy 插件

会根据项目将插件下载到系统环境或者项目环境下
```
File --> Project Structure --> SDKs --> Packages
```

## scrapy项目结构

```sh
项目名
    项目名
        spiders
            __init__.py
            自定义爬虫文件.py
        __init__.py
        items.py
        middlewares.py
        pipelines.py
        settings.py
    scrapy.cfg


# spiders：存放自定义爬虫文件的目录
# items.py：定义数据结构的地方，是一个继承自scrapy.Item的类
# middlewares.py：中间件 代理
# pipelines.py：管道文件，里面只有一个类，用于处理下载数据的后续处理默认是300优先级，值越小优先级越高（1‐1000）
# settings.py：配置文件 比如：是否遵守robots协议，User‐Agent定义等

```

## scrapy基本使用
找到scrapy.exe的位置，根据安装位置的不同，
```sh
# 创建新项目
scrapy startproject [项目名]


# 创建脚本文件，文件名为baidu， 地址为 www.baidu.com
scrapy genspider baidu www.baidu.com
```

根据模板创建出来的 baidu.py 脚本
```py
import scrapy

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["www.baidu.com"]
    start_urls = ["https://www.baidu.com"]

    def parse(self, response):
        # 网页源码，字符串格式
        response.text
        # 网页源码，二进制格式
        response.body
        # 使用xpath解析
        response.xpath()
        
```

```
scrapy crawl [爬虫文件的属性name]
scrapy crawl baidu
```
