from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time





# 浏览器驱动文件位置
service = Service('chromedriver.exe')

# chrome参数
chrome_options = Options()
chrome_options.add_argument('--headless')

# 得到浏览器
browser = webdriver.Chrome(service=service, options=chrome_options)

# 打开网页
browser.get('https://www.baidu.com')
time.sleep(2)

# 输入框中输入
browser.find_element(by=By.ID, value='kw').send_keys('随便输入点什么')
time.sleep(2)

# 点击百度一下按钮
browser.find_element(by=By.ID, value='su').click()
time.sleep(2)


