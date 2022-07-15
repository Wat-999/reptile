# 2.1 常规手段爬取微信推文（简易版）
import requests
import re
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# 1.获取网页源代码
url = 'https://weixin.sogou.com/weixin?type=2&query=阿里巴巴'
res = requests.get(url, headers=headers, timeout=10).text
print(res)

#学会在打印的源代码中寻找正则规律，看其头尾，注意网址的拼接
# 2.编写正则表达式
p_title = 'uigs="article_title_.*?">(.*?)</a>'  # 标题
p_source = 'uigs="article_account_.*?">(.*?)</a>'  # 新闻来源
p_date = 'timeConvert\(\'(.*?)\'\)'  # 日期  利用时间戳做的正则提取
p_href = '<div class="txt-box">\n<h3>\n<a target="_blank" href="(.*?)"'  # 网址  其中\n表示换行，也可以用.*?代替换行
title = re.findall(p_title, res)
source = re.findall(p_source, res)
date = re.findall(p_date, res)
href = re.findall(p_href, res, re.S)  # 因为有换行，所以要加上re.S

# 3.清洗并打印数据
for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])  #清理标题中的"<em>、</em>、只要是<任意内容>"
    title[i] = re.sub('&.*?;', '', title[i])   #清洗"$.*?:"格式的内容
    timestamp = int(date[i]) #用正则提取出来的是字符串，因此用int()函数将其转为数字
    timeArray = time.localtime(timestamp)  #将时间戳转换为常规格式的日期
    date[i] = time.strftime("%Y-%m-%d", timeArray)  #指定日期格式
    href[i] = 'https://weixin.sogou.com' + href[i]
    print(str(i+1) + '.' + title[i] + '(' + date[i] + ' ' + source[i] + ')')
    print(href[i])

