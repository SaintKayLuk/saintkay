## selenium

模拟真实浏览器访问，需要浏览器驱动内核

chrome驱动下载地址
```
http://chromedriver.storage.googleapis.com/index.html
```



#### 使用selenium访问网页
```py
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# 添加 chromedriver.exe 的实际路径
service = Service('chromedriver.exe')
browser = webdriver.Chrome(service=service)
browser.get('https://www.jd.com')

# 获取网页标题
browser.title
# 获取浏览器名称
pbrowser.name
# 获取网页源码
browser.page_source
```


#### 元素定位

```py
from selenium.webdriver.common.by import By

# 根据id查找元素
browser.find_element(by=By.ID, value='')
# 根据name查找元素
browser.find_element(by=By.NAME, value='')
# 根据xpath语法来查找元素
browser.find_element(by=By.XPATH, value='')
# 根据链接名字，查找链接的标签元素
browser.find_element(by=By.LINK_TEXT, value='')
```

#### 元素信息

```py

# 根据id为a查找到某元素
label = browser.find_element(by=By.ID, value='a')

# 获取value属性的值
label.get_attribute('value')
# 获取标签名，例如此标签是input标签，a标签之类的
label.tag_name
# 获取标签内容，两个标签中间部分 <span>xxx</span>
label.text
```

#### 模拟浏览器操作

以百度搜索为例，模拟认为操作，每部操作之间都等待2秒
```py

# 获取搜索框，并输入
inp = browser.find_element(by=By.ID, value='kw')
inp.send_keys('哈哈')
time.sleep(2)

# 获取 百度一下 按钮，并点击
button = browser.find_element(by=By.ID, value='su')
button.click()
time.sleep(2)

# 鼠标滚到到地步
browser.execute_script('document.documentElement.scrollTop=100000')
time.sleep(2)

# 获取下一个按钮，并点击
next = browser.find_element(by=By.CLASS_NAME, value='n')
next.click()
time.sleep(2)

# 浏览器回退
browser.back()
time.sleep(2)

# 浏览器前进
browser.forward()
time.sleep(2)

# 退出浏览器
browser.quit()
```

#### handless

无界面使用浏览器
```py
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

service = Service('chromedriver.exe')

# 添加参数
chrome_options = Options()
chrome_options.add_argument('--headless')

# 传递 service 和 option
browser = webdriver.Chrome(service=service, options=chrome_options)
```

