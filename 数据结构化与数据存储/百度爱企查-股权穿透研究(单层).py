#单层股权结构爬取

from selenium import webdriver
import re
import time
import pandas as pd

company_name = '华能信托'
browser = webdriver.Chrome()
url = 'https://xin.baidu.com/s?q=' + company_name  #拼接网址，可供多家公司
browser.get(url)  #打开网址
data = browser.page_source  #获取网页源代码
#print(data)

#正则提取
p_href = '<a data-v-387da8b0="" target="_blank" href="(.*?)"'
href = re.findall(p_href, data)
#因为提取到到详情页面网址并不完整，还需要为其拼接前缀
url2 = 'https://xin.baidu.com' + href[0]  #注意href是一个列表，通常搜索结果页面的第一个网址就是最匹配搜索关键词的公司的详情页面网址
browser.get(url2)
data = browser.page_source

#获取表格
table = pd.read_html(data)
df = table[1]  #通过尝试，发现第2个表格是所需的股权结构，故用table[1]
print(df)

#提取第一大控股股东，即发起人/股东的第1行
company = df['股东名称'][0]
#随后还需要对提取的内容进行处理。从图上可以看出，'发起人/股东'列中的信息有些杂乱，每家公司的全称后都有'股权结构>'字样
#有的公司全称前还有简称，例如，第二大股东前有"乌江能源"字样。因为这些内容都是通过空格分隔的，
company_split = company.split(' ')    #根据空格拆分字符串
for i in company_split:  #遍历拆分后的内容
    if len(i) > 6:      #如果内容的字符数大于6(通常公司全称都会大于6个字),则其是所需内容
        print(i)
