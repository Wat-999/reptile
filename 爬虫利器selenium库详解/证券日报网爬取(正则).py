import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

# 1.获取网页源代码
url = 'http://search.zqrb.cn/search.php?src=all&q=贵州茅台&f=_all&s=newsdate_DESC'
res = requests.get(url, headers=headers).text
# print(res)

# 2.解析网页源代码提取信息
p_title = '<a href=".*?" target="_blank"><h4>(.*?)</h4></a>'
p_href = '<a href="(.*?)" target="_blank"><h4>.*?</h4></a>'
p_date = '<span><strong>时间:</strong>(.*?)</span>'
title = re.findall(p_title, res)
href = re.findall(p_href, res)
date = re.findall(p_date, res)

# 3.清洗 & 打印数据
source = []  # 新建一个列表，用来拼接新闻来源，这里都是证券日报
for i in range(len(title)):
    source.append('证券日报')
    title[i] = re.sub('<.*?>', '', title[i])  # 有的标题里有<em></em>这样的标签，这里清洗下数据
    date[i] = date[i].split(' ')[0]  # 日期只需要2020-11-18 06:15:27的年月日信息
    print(title[i] + '(' + source[i] + ' ' + date[i] + ')')  # 提取的标题自带序号
    print(href[i])

