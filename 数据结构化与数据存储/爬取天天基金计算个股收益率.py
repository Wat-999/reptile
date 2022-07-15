import requests
import re
import pandas as pd
import tushare as ts
import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
url = 'http://fund.eastmoney.com/004857.html'  # 这个都是A股，比较正常
res_test = requests.get(url, headers=headers).text

res_test = res_test.encode('ISO-8859-1').decode('utf-8')  #转换编码格式

#print(res_test)  #检验是否还有乱码

# 获取该基金的基金规模与起始日期
p_amount = '基金规模</a>：(.*?)亿元'  # 基金规模
p_date = '成 立 日</span>：(.*?)</td>'  # 起始日期

amount = re.findall(p_amount, res_test)
date = re.findall(p_date, res_test)

print(amount, date)


#获取基金中个股的比例
table = pd.read_html(res_test)  # table是一个列表，里面有该网页里的所有表格
stock = table[5]  # 试一下就知道是table中的哪个表格了，这个股票持仓对应的是table[5]
#stock.columns = stock.iloc[0]  # 这个因为它把列索引也当做一行了，所以要进行如下处理，这行是将列索引换成原表格的第一行
stock = stock[1:]  # 从原表格的第二行开始选择
print(stock)

# 注意这里先不要进行清除股票名称中可能存在的空格，例如把“五粮液”写成“五 粮 液”，因为之后需要利用原文字写正则
# stock = stock.copy()
# stock['股票名称'] = stock['股票名称'].apply(lambda x:x.replace(' ', ''))
# stock

#利用接口去匹配数据
today = datetime.datetime.now()   #当前时间
today = today.strftime('%Y%m%d')  #转换成字符串格式 ，带p的是转换为时间格式

date[0] = date[0].replace('-', '')  #装换格式，与

pro = ts.pro_api('9d674d000f7c730dd3108701a1a1c534bf51bfb03a0ff169a9d11848')      #ts.pro_api(注册获得token填在这里)  有2100积分
df_stock = pro.daily(ts_code='600585.SH', start_date=date[0], end_date=today)#pro.daily（'股票代码'，start='起始日期'， end='结束日期'）函数获取上市公司万科十年的股票日线级别的数据
#https://tushare.pro/user/token
# 一次性获取全部日k线数据，注意date是一个列表，所以用[0]提取第一也是唯一的元素，code之后还会批量爬
print(df_stock.head(), df_stock.tail())

# 计算成立日期以来的收益率；如果要计算百分位数，这里乘以100即可，这里先不乘以100
ratio = df_stock.iloc[-1]['close'] / df_stock.iloc[0]['close'] - 1   #close表示的是当天的收盘价
print(ratio)