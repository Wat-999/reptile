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
#stock = stock[0:]  # 从原表格的第二行开始选择
#print(stock)


#提取股票序号
p_code = '<td class="alignLeft">   <a href="//quote.eastmoney.com/unify/r/\d.(.*?)" title='  #这里只能提取股票序号其格式为00002
#这里有\d匹配1个数字字符，就免了后面的数据清洗
# 这里注意如果有sh（上交所）打头，有的是sz（深交所）打头，先都提取再处理

codes = re.findall(p_code, res_test)
#print(code)

#拼接成Tushare Pro可以识别的 000860.SZ格式
code = []
for i in range(len(codes)):  #对股票序号进行判断
    if codes[i][0] == str(6):
       code.append(codes[i] + "." + "sh")

    elif codes[i][0] == str(0):
        code.append(codes[i] + "." + "sz")

    elif codes[i][0] == str(4) or codes[i][0] == str(8):
        code.append(codes[i] + "." + "bj")

    else:
        codes[i] = codes[i] + "." + "hg"
        code.append(codes[i])
#print(code)

#复制原有的表格，并新增一列为股票代码
stock = stock.copy()  #浅拷贝，不改变原表格
stock['股票代码'] = code
#print(stock)


# 计算所有股票自成立来的涨跌信息
pro = ts.pro_api('9d674d000f7c730dd3108701a1a1c534bf51bfb03a0ff169a9d11848')      #ts.pro_api(注册获得token填在这里)  有2100积分
ratio_list = []
for i, row in stock.iterrows():  # 不清楚iterrows()用法的可以把i和row打印出来看下，其中i为行索引序号，row为该行对应的内容
    today = datetime.datetime.now()
    today = today.strftime('%Y%m%d')  # 注意Tushare Pro接收的日期格式

    # 提取股票信息
    if 'hk' in row['股票代码']:  # 默认要么A股，要么港股
        df_stock = pro.hk_daily(ts_code=row['股票代码'], start_date=date[0],
                                end_date=today)  # date[0]是之前爬到的基金成立日期，这个还需完善，因为不一定是成立的时候买的股票
    else:
        df_stock = pro.daily(ts_code=row['股票代码'], start_date=date[0], end_date=today)

    # 计算自成立以来的收益率
    ratio = df_stock.iloc[-1]['close'] / df_stock.iloc[0]['close'] - 1

    ratio = round(ratio, 3)  # 取3位小数round()函数

    # 把各个股票的收益率整合到一起
    ratio_list.append(ratio)

#print(ratio_list)
stock['个股收益率'] = ratio_list
print(stock)