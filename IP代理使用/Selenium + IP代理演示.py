import requests
from selenium import webdriver
proxy = requests.get('http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=890fff42d97343ecbb39c346691044d9&orderno=YZ20225168198U2P78s&returnType=1&count=10').text
proxy = proxy.strip()  # 这一步非常重要，因为要把你看不见的换行符等空格给清除掉

# 使用代理
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=' + proxy)
browser = webdriver.Chrome(options=chrome_options)

url = 'https://httpbin.org/get'
browser.get(url)

data = browser.page_source
print(data)
