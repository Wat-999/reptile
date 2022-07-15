#在弹出的页面中可查看资产负债表、利润表、现金流量表等财务报表
#如果想爬取利润表或现金流量表，可用开发者工具获取相应链接等XPATH表达式，再用selenium库模拟单击链接切换页面
#用Tushare Pro 也能获取财务报表
import pandas
from selenium import webdriver
import pandas as pd
browser = webdriver.Chrome()
browser.maximize_window()  # 最大化网页，非必须
url = 'https://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/600519/ctrl/part/displaytype/4.phtml'
browser.get(url)
data = browser.page_source  #获取网页源代码
table = pandas.read_html(data)  #table是一个包含网页中所有表格数据的列表
#网页表格众多，需要确定资产负债表在第几个表格。通过用for循环语句遍历列表table，然后依次打印输出各个表格的序号和内容
for i in range(len(table)):
    print(i)
    print(table[i])
#打印输出结果如下，可以看到序号为14的表格(即第15张表格)是我们需要的资产负债表
#因此，通过table[14]即可提取所需数据
df = table[14]
print(df)
#打印输出结果看到列索引(表头)有点问题，这是因为原表格的表头中有合并单元格
#这里我们希望把打印结果中的第一行数据设置为列索引，然后从第2行开始选取表格数据并且删除含有空值的行
df.columns = df.iloc[0]   #设置列索引为原表格的第1行
df = df[1:]    #从第二行选取数据
df = df.dropna()   #删除含有空值的行
# df = df.dropna(how='all')   #删除全为空值的行
# df = df.dropna(thresh=2)    #表示行内至少要有两个空值，否则删除该行

#最后将数据导出为excel工作簿
df.to_excel('贵州茅台-资产负债表.xlsx', index=False)  #设置index=False以忽略行索引