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

# 进行翻页（不分页）操作
browser.find_element(By.XPATH, '/html/body/div[7]/div[4]/div[3]/label/span').click()  # 这里居然有一个不分页的按扭，那这样就更好爬了
#注意要导入from selenium.webdriver.common.by import By
#否则报错name'By'未定义
time.sleep(10)

data = browser.page_source   #打印网页源代码
table = pd.read_html(data)  # table是一个列表，里面有该网页里的所有表格
df = table[3]  # 试一下就知道是table中的哪个表格了，单页的话时table[3]
print(df.head())
print(df.shape)