import requests
from bs4 import BeautifulSoup
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

url = 'http://search.zqrb.cn/search.php?src=all&q=贵州茅台&f=_all&s=newsdate_DESC'
res = requests.get(url, headers=headers).text
# print(res)
soup = BeautifulSoup(res, 'html.parser')  # 根据HTML网页字符串创建BeautifulSoup对象,'html.parser'能解析

a = soup.select('dt a')
p_date = '<span><strong>时间:</strong>(.*?)</span>'  # 这个日期如果用BS写起来稍微有点麻烦，还不如正则来写
date = re.findall(p_date, res)

for i in range(len(a)):
    print(a[i].text)  # 这里的标题自带序号
    print(a[i]['href'])