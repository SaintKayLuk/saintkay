
## urllib

python自带的一个库，能够模拟浏览器请求

### 发送请求

##### 直接请求
```py
import urllib.request

# 访问百度
url = 'http://www.baidu.com'

# 直接传url，返回的response为 http.client.HTTPResponse 类型
response = urllib.request.urlopen(url)
```

##### 自定义request
```py
# 在header里添加 user-agent
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Cookie': 'xxx'

}
# 在request中添加headers
request = urllib.request.Request(url=url, headers=headers)

# 发送请求，传递request
response = urllib.request.urlopen(request)
```







##### hander

处理复杂的请求

```py
request = urllib.request.Request(url=url, headers=headers)

# 实现代理功能的handler
handler = urllib.request.ProxyHandler()
# 实现验证功能的handler
handler = urllib.request.HTTPBasicAuthHandler()
# 实现cookie功能
handler = urllib.request.HTTPCookieProcessor()


# 获取opener对象
opener = urllib.request.build_opener(handler)

# 调用open方法，相当于urllib.request.urlopen(request)
response = opener.open(request)
```



#### 中文转Unicode

```py
import urllib.parse

# 创建一个字典
data = {
    'wd': '周杰伦',
    'sex': '男',
    'location': '中国台湾省'
}

# 转换为 unicode并且以&相连，例如 xxx&xxx
urllib.parse.urlencode(data)
```

### get请求和post请求


```py
url = 'http://xxx'
heaers = {
    'xx': 'xxx'
}
# 转义headers
headers = urllib.parse.urlencode(headers)
# 传url和 headers 则为get请求
request = urllib.request.Request(url=url, headers=headers)

# 添加post请求参数
data = {
    'xx': 'xxx'
}
# 转义data数据，并且编码为byte
data = urllib.parse.urlencode(data).encode('utf-8')
# 传data则为post请求
request = urllib.request.Request(url=url, data=data, headers=headers)
```

### 返回内容
```py
response = urllib.request.urlopen(url)
# 返回为字节，解码为utf-8格式
response.read().decode('utf-8')

# 读取指定字节
response.read(5)

# 读取一行
response.readline()

# 读取所有行，并存为列表
response.readlines()

# 获取http状态码
response.getcode()
```

下载
```py
# 根据url地址可下载网页，图片，视频等
url = 'xxx'

# 自定义保存的名字，例如下载图片，一般后缀改为jpg，png等，但是不影响文件本身
urllib.request.urlretrieve(url, filename = 'xxx')
```


### 异常


```PY
import urllib.error.HTTPError
import urllib.error.URLError
```



