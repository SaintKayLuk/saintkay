## requests

使用request库发起请求


### 发起请求
```py
import requests

url = 'http://www.baidu.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
#get请求的参数
params = {
    'key': 'value'
}
#post请求参数
data = {
    'key': 'value'
}

# post请求json参数
json = '{"key1":"value1","key2":"value2"}'


#get请求
response = requests.get(url=url, params=params, headers=headers)

#post请求
response = requests.post(url=url, data=data, json=json, headers=headers)
```

### 返回结果
```py
# 设置响应的编码格式
response.encoding = 'utf-8'

# 以字符串的形式来返回了网页的源码
response.text

# 返回请求的url地址
response.url

# 返回二进制数据
response.content

# 返回响应的状态码
response.status_code
```

### 使用代理

```py

proxies = {
    'http': '1.1.1.1:8888'
}

response = requests.get(url=url, headers=headers, proxies=proxy)
```


### session

使用session，多次请求为同一个对象

```py
import requests
session = requests.session()

# 和requests.get(),requests.post()方法一样
session.get()
session.post()
```

