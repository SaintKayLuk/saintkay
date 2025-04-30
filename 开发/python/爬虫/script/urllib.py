import urllib.request
import urllib.error
import urllib.parse




# 简单get请求模板
def http_get():
    url = 'http://www.xxx.com'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    try:
        urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        print(content)
    except urllib.error.HTTPError:
        pass
    except urllib.error.URLError:
        pass

# 简单post请求模板
def http_post():
    url = 'http://www.xxx.com'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    # post表单内容
    data = {
        'key': 'value'
    }
    # 编码data数据
    data = urllib.parse.urlencode(data).encode('utf-8')
    try:
        urllib.request.Request(url=url, data=data, headers=headers)
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        print(content)
    except urllib.error.HTTPError:
        pass
    except urllib.error.URLError:
        pass


if __name__ == '__main__':
    http_get()
    http_post()