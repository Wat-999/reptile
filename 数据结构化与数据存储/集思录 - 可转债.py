from selenium import webdriver
import pandas as pd
import time

browser = webdriver.Chrome()
url = 'https://www.jisilu.cn/data/cbnew/#cb'
browser.get(url)
time.sleep(30)   #用来登录，因为游客只能获取到少量数据
data = browser.page_source
time.sleep(10)  #防止网页没加载完，导致获取不到数据，
tables = pd.read_html(data)  #如果报错未找到匹配模式 '.+' 的表，就在前面加个休息时间
df = tables[0]
#print(df)
df.columns = ['代 码', '转债名称', '现 价', '涨跌幅', '正股名称', '正股价', '正股涨跌', '正股PB', '转股价', '转股价值', '溢价率', '纯债价值', '评级', '期权价值', '回售触发价', '强赎触发价', '转债占比', '机构持仓', '到期时间', '剩余年限', '剩余规模(亿元)', '成交额(万元)', '换手率', '到期税前收益', '回售收益', '双低', '操作', '下修条件', '地域']
print(df)
