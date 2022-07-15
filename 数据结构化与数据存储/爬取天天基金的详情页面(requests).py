import requests
import re
import pandas as pd
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
url = 'http://fund.eastmoney.com/006675.html'
res = requests.get(url, headers=headers).text

#解决编码问题
try:
    res = res.encode('ISO-8859-1').decode('utf-8')  # 方法3
except:
    try:
        res = res.encode('ISO-8859-1').decode('gbk')  # 方法2
    except:
        res = res  # 方法1

#print(res)


# 获取该基金的基金规模与起始日期
p_amount = '基金规模</a>：(.*?)亿元'  # 基金规模
p_date = '成 立 日</span>：(.*?)</td>'  # 起始日期

amount = re.findall(p_amount, res)
date = re.findall(p_date, res)

print(amount, date)


#获取基金中个股的比例
table = pd.read_html(res)  # table是一个列表，里面有该网页里的所有表格
stock = table[5]  # 试一下就知道是table中的哪个表格了，这个股票持仓对应的是table[5]
#stock.columns = stock.iloc[0]  # 这个因为它把列索引也当做一行了，所以要进行如下处理，这行是将列索引换成原表格的第一行
stock = stock[1:]  # 从原表格的第二行开始选择
print(stock)

# 清除股票名称中可能存在的空格，例如（http://fund.eastmoney.com/003634.html）会把“五粮液”写成“五 粮 液”，这样导致之后就难以匹配行业了。
stock = stock.copy()
stock['股票名称'] = stock['股票名称'].apply(lambda x: x.replace(' ', ''))  #空格处理


# 根据基金规模和个股持仓，计算个股的金额
stock = stock.copy()
stock['持仓金额(亿元)'] = stock['持仓占比'].apply(lambda x: float(x[0:-1])/100) * float(amount[0])  # 注意格式转换，以及除以100
# 不能直接用int，那个是取整的，而且不能小于1的数。
print(stock)

