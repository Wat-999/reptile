import pandas as pd
import re
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://data.eastmoney.com/report/stock.jshtml')
data = browser.page_source
table = pd.read_html(data)[1]   #获取表格
#print(table)
#print(table.columns)

#正则提取href
p_href = '<td><a href="(.*?)">'
href_d = re.findall(p_href, data)
href_s = ','.join(href_d)
a = 'class="red,(.*?),'
href = re.findall(a, href_s)
#print(href)
print(len(href))  #检查数据是否有误

#拼接研报的网址(提取的网址只有后缀)
for i in range(len(href)):
    href[i] = 'https://data.eastmoney.com/' + href[i]
    #print(href[i])

#将研报数转换成字符串
table = table.astype('str')  # 因为研报数是数字，所以需要转为字符串，或者直接用str()函数转换研报数那一列的内容，写成str(row['近一月个股研报数']['近一月个股研报数'])
#astype()函数可用于转化dateframe某一列的数据类型，其格式为.astype('需要转换的类型')

for i, row in table.iterrows():
    print(str(i + 1) + '.' + row['股票简称']['股票简称'])   #这里为什么写row['股票简称']['股票简称']，因为读取下来表头是双层的
    print('研报日期：' + row['日期']['日期'])
    print('研报标题：' + row['报告名称']['报告名称'])
    print('公司评级：' + row['东财评级']['东财评级'])
    print('评级变化：' + row['评级变动']['评级变动'])
    print('近一月个股研报数：' + row['近一月个股研报数']['近一月个股研报数'])
    print('研报链接：' + href[i])
    print('------------------------')