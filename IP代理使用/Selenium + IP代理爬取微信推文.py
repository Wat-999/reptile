from selenium import webdriver
import re
import time
import requests
proxy = requests.get('http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=890fff42d97343ecbb39c346691044d9&orderno=YZ20225168198U2P78s&returnType=1&count=10').text
proxy = proxy.strip()  # 这一步非常重要，因为要把你看不见的换行符等空格给清除掉

# 使用代理
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=' + proxy)
browser = webdriver.Chrome(options=chrome_options)
url = 'https://weixin.sogou.com/weixin?type=2&query=阿里巴巴'
browser.get(url)
data = browser.page_source
# print(data)

# 2.编写正则表达式
p_title = 'uigs="article_title_.*?">(.*?)</a>'  # 标题
p_source = 'uigs="article_account_.*?">(.*?)</a>'  # 新闻来源
p_date = 'timeConvert\(\'(.*?)\'\)'  # 日期
p_href = '<div class="txt-box">\n<h3>\n<a target="_blank" href="(.*?)"'  # 网址  其中\n表示换行，也可以用.*?代替换行
title = re.findall(p_title, data)
source = re.findall(p_source, data)
date = re.findall(p_date, data)
href = re.findall(p_href, data, re.S)

# 3.清洗并打印数据
for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])  # 清理标题中的"<em>、</em>、只要是<任意内容>"
    title[i] = re.sub('&.*?;', '', title[i])  # 清洗"$.*?:"格式的内容
    timestamp = int(date[i])  # 用正则提取出来的是字符串，因此用int()函数将其转为数字
    timeArray = time.localtime(timestamp)  # 将时间戳转换为常规格式的日期
    date[i] = time.strftime("%Y-%m-%d", timeArray)  # 指定日期格式
    href[i] = 'https://weixin.sogou.com' + href[i]
    print(str(i + 1) + '.' + title[i] + '(' + date[i] + ' ' + source[i] + ')')
    print(href[i])