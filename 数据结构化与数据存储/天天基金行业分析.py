import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
url = 'http://fund.eastmoney.com/006675.html'
res = requests.get(url, headers=headers).text
res = res.encode('ISO-8859-1').decode('utf-8')  # 方法3

#这边得加一下各个公司的金额，这样才知道擅长领域；或者该基金经理管理的基金也不会太多，就给他分几个分支就行
# 获取该基金的基金规模与起始日期
p_amount = '基金规模</a>：(.*?)亿元'  # 基金规模
p_date = '成 立 日</span>：(.*?)</td>'  # 起始日期

amount = re.findall(p_amount, res)
date = re.findall(p_date, res)

print(amount, date)


#获取基金中个股的比例
table = pd.read_html(res_test)  # table是一个列表，里面有该网页里的所有表格
stock = table[5]  # 试一下就知道是table中的哪个表格了，这个股票持仓对应的是table[5]
#stock.columns = stock.iloc[0]  # 这个因为它把列索引也当做一行了，所以要进行如下处理，这行是将列索引换成原表格的第一行
#stock = stock[0:]  # 从原表格的第二行开始选择
#print(stock)

# 清除股票名称中可能存在的空格，例如（http://fund.eastmoney.com/003634.html）会把“五粮液”写成“五 粮 液”，这样导致之后就难以匹配行业了。
stock = stock.copy()   #浅拷贝，不改变原表格
stock['股票名称'] = stock['股票名称'].apply(lambda x:x.replace(' ', ''))
print(stock)

#根据基金规模和个股持仓，计算个股的金额
stock['持仓占比'] = stock['持仓占比'].apply(lambda x: float(x[:-1]))  # 清洗下持仓占比，等会需要加和操作，现在是字符串不好操作
stock = stock.copy()
stock['持仓金额(亿元)'] = stock['持仓占比'].apply(lambda x: x/100) * float(amount[0])  # 注意格式转换，以及除以100

# 读取A股、深股、北股、港股上市公司行业信息,然后去匹配行业
data = pd.read_excel('A股上市公司基本资料.xlsx')
data_hk = pd.read_excel('港股上市公司基本资料.xlsx')

industry = []
for i in stock['股票名称']:
    try:
        industry.append(data[data['证券简称'] == i]['行业'].iloc[
                            0])  # 这里可以先用print打印看看stock['股票名称']，然后这里有个注意点，因为获取的是series，有索引，所以需要通过iloc[0]选择内容，不理解，可以将append()函数中的 data[data['证券简称'] == i]['行业'] 内容打印一下
    except:
        industry.append(data_hk[data_hk['证券简称'] == i]['行业'].iloc[0])  # 目前国内还是主要交易 A股和 港股

print(industry)

stock = stock.copy()  # copy是浅拷贝，改变复制后的内容，原内容不会变，这里其实可以不写这一行，不过不写的话，它会有个警告，也挺烦人的。
stock['行业'] = industry

print(stock)


#获取前10个股票的名称 + 行业
stock_name_list = list(stock['股票名称'] + '(' + stock['行业'] + ')')  #列拼接
stock_name = ', '.join(stock_name_list)
print(stock_name)

#统计行业信息(看看重仓哪个行业)：用groupby方法更好，还可以统计比例
ratio_sum = stock.groupby('行业')[['持仓占比']].sum()
ratio_sum = ratio_sum.sort_values('持仓占比', ascending=False)  ## 降序排列

main_industry_list = list(ratio_sum.index)  #提取行索引这一列，并放在列表里
main_industry_ratio = list(ratio_sum['持仓占比']) #提取列'持仓占比'
print(main_industry_list, main_industry_ratio)

#计算金额总和
money_sum = stock.groupby('行业')[['持仓金额(亿元)']].sum()
money_sum = money_sum.sort_values('持仓金额(亿元)', ascending=False)
print(money_sum)