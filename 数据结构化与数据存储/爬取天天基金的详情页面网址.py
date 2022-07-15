import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

# 通过selenium库访问网站，这个首页不能通过requests库爬，但是里面的单个网页反而可以
browser = webdriver.Chrome()
browser.maximize_window()  # 最大化网页
url = 'http://fund.eastmoney.com/data/fundranking.html#tgp'  # 这个链接中的tgp表示的就是股票型基金，如果是混合型，则为thh
browser.get(url)

browser.find_element(By.XPATH, '/html/body/div[7]/div[4]/div[3]/label/span').click()  # 这里居然有一个不分页的按扭，那这样就更好爬了
#注意要导入from selenium.webdriver.common.by import By
#否则报错name'By'未定义
time.sleep(15)

data = browser.page_source
table = pd.read_html(data)  # table是一个列表，里面有该网页里的所有表格
df = table[3]  # 试一下就知道是table中的哪个表格了，单页的话时table[3]
print(df.head())
print(df.shape)
# 导出成Excel
df.to_excel('股票型基金.xlsx', index=False)

# 获取每个基金的网址信息
p_title_A = '<a href=".*?" title="(.*?)">.*?</a>'  # 基金全称
p_title_B = '<a href=".*?" title=".*?">(.*?)</a>'  # 基金简称
p_href = '<a href="(.*?)" title=".*?">.*?</a>'  # 基金链接，这个链接获取起来比较麻烦，正则不太好写，但是经过观察，发现可以通过基金代码code来弄

title_A = re.findall(p_title_A, data)
title_B = re.findall(p_title_B, data)
href = re.findall(p_href, data)
#print(href)

for i in range(len(title_A)):
    href[i] = href[i].split('<a href="')[-1]  # 这个处理技巧比较精妙，因为它那个正则比较难写，但是原href[i]最后就是需要的网站，所以这么提取，也可以通过code编

    print(str(i+1) + '.' + title_A[i] + '-' + title_B[i])
    print(href[i])

df['网址'] = href
df['基金全称'] = title_A
print(df.head())

#如果想把正则表达式p_href的'文本a写得更严谨些，需要稍微动些脑筋。通过观察发现，"<a href="详情页面网址"title"基金全名称>基金简称</a>
#前面通常会有6位数的基金代码"</a></td><td>",因此，p_href更严格的写法如下：
# p_href = '\d\d\d\d\d\d</a></td><td><a href="(.*?)" title='