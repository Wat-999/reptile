import requests
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
url = 'http://news.sina.com.cn/china/'
res = requests.get(url, headers=headers).text
try:
    res = res.encode('ISO-8859-1').decode('utf-8')   #方法3
except:
    try:
        res = res.encode('ISO-8859-1').decode('gbk')   #方法2
    except:
        res = res
# code = requests.get(url, headers=headers).encoding   #查看python获取的网页源代码的编码格式
# res.encoding = 'utf-8'   #先对获取的网页响应进行编码处理，再提取文本
# #网页源代码中出现乱码的原因主要是python获取的网页源代码格式和网页实际的编码格式不一致，常见的编码格式有utf-8，gbk，iso-8859-1
# #可一用开发者工具查看网页源代码，然后展开<head>标签，查看<meta>标签的charset属性，可以知道网页的编码格式
# res = res.text
# print(code)

soup = BeautifulSoup(res, 'html.parser')  #激活BeautifulSoup库，'html.parser'表示设置解析器为HTML解析器，res为网页源代码

a = soup.select('.news-1 li a') + soup.select('.news-2 li a')
#这里有两点需要注意：第一：select('.news-1 li a')使用多层次筛选功能(class属性)，先用'.news-1'筛选class属性为'news-1'的标签
#在用'li a'继续往下筛选<li>标签下的<a>标签，第二这里直接把两个select()函数的筛选结果用"+"号连接起来，类似于列表的拼接，实现选取的结果汇总


print(a)

for i in range(len(a)):
    print(str(i+1) + '.' + a[i].text)  #用text属性提取标题，
    print(a[i]['href'])  #用['href']属性提取网址

# 补充说明：如果想保存新闻标题或者网址，可以使用如下代码：
title = []
href = []
for i in range(len(a)):
    title.append(a[i].text)
    href.append(a[i]['href'])
# print(title)
# print(href)

