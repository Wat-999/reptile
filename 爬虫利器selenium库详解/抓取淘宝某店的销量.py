import time
import re
from selenium import webdriver
import pandas as pd

browser = webdriver.Chrome()
url = 'https://runbaiyan.tmall.com/search.htm?spm=a1z10.1-b-s.w5001-21884551106.3.3f0d7f68FOYkqz&search=y&scene=taobao_shop'
browser.get(url)
# 打开网页后暂停30秒用于手动登陆网站，推荐手机APP扫码登录，会快一些
time.sleep(30)
data = browser.page_source
# print(data)
# browser.quit()

p_sales = '<span class="sale-num">(.*?)</span>'
sales = re.findall(p_sales, data, re.S)  #销量
p_price = '<span class="c-price">(.*?)</span>'
price = re.findall(p_price, data, re.S)  #价格
p_name = '<a class="item-name .*?}">(.*?) </a>'
name = re.findall(p_name, data, re.S)  #名称
print(name)
print(sales)
print(price)

for i in range(len(name)):
    name[i] = re.sub('data.*?jpg', '', name[i])  # 清除名称中一些杂乱元素
    price[i] = price[i].strip()  # 清除价格两旁的空格
    print('商品名称为：' + name[i])
    print('商品价格为：' + price[i])
    print('商品销量为：' + sales[i])

file_name = time.strftime('%Y-%m-%d') + '润百颜销量情况' + '.xlsx'
print(file_name)  # 打印下构造的文件名
df = pd.DataFrame({'名称': name, '销量': sales, '价格': price})  # pandas相关知识点可以参考第6章
df.to_excel(file_name, index=False)


#用正则表达式提取的内容为字符串，而价格和销量通常作为数字来处理，因此，可以通过如下代码把价格装换为数字格式
# for i in range(len(price)):
#     price[i] = float(price[i])    #用float()函数用于将小数格式的字符串装换为数字
#     sales[i] = int(sales[i])     #int()函数用于将整数格式的字符串转换为数字







