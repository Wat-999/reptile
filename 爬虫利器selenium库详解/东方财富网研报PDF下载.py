#还需改造才能实现多页批量下载(需要模拟点击下一页)
#用re提取一定多找规律，一步不能到达，就拆分成几步实现。  实现多页需解决模拟单击问题
import time
from selenium import webdriver
import pandas as pd
import re

def get_URL():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)

    for i in range(1, 23):
        url = 'http://so.eastmoney.com/Yanbao/s?keyword=%E6%A0%BC%E5%8A%9B%E7%94%B5%E5%99%A8&pageindex=' + str(i)
        # print(url)
        browser.get(url)
        data = browser.page_source
        # print(data)

        # 正则提取
        p_href = '<span class="notice_item_t_label">【<span>格力电器</span>】</span><a href="(.*?)" target="_blank'  # 这个得写的稍微严格一点，不然非贪婪会导致第一条信息匹配不全

        href = re.findall(p_href, data, re.S)
        # print(href)
        # 将所有研报的URL进行保存
        for j in range(len(href)):
            href_all.append(href[j])


def download_PDF(url):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    data = browser.page_source
    # print(data)
    name = '<h1>(.*?)</h1>'
    file_name = re.findall(name, data, re.S)
    # 正则提取
    href = '<a class="rightlab" href="(.*?)">【点击查看PDF原文】</a>'  # 这个得写的稍微严格一点，不然非贪婪会导致第一条信息匹配不全

    #
    pdf_href = re.findall(href, data, re.S)
    print(pdf_href)

    # print(name, industry, phone, email)
    try:
        import requests
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
        res = requests.get(pdf_href[0], headers=headers)
        path = '/Users/macbookair/Desktop/格力研报/' + file_name[0].strip() + '.pdf' #拼接文件的名称，文件所在目录提前创建好
        file = open(path, 'wb')
        file.write(res.content)
        file.close()
    except:
        print("error")



import re

href_all = []
get_URL()  #获取所有研报的URL

print(href_all)
# 打开每一个研报界面并下载对应的PDF
for url in href_all:
    download_PDF(url)

# print(href_all)









