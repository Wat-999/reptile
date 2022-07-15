from selenium import webdriver
import re
import time
import pandas as pd

def baidu(company_name):
    browser = webdriver.Chrome()
    url = 'https://xin.baidu.com/s?q=' + company_name
    browser.get(url)
    time.sleep(2)  # 休息2秒，防止页面没加载完
    data = browser.page_source

    p_href = '<a data-v-387da8b0="" target="_blank" href="(.*?)"'
    href = re.findall(p_href, data)
    url2 = 'https://xin.baidu.com' + href[0]
    browser.get(url2)
    time.sleep(2)  # 休息2秒，防止页面没加载完
    data = browser.page_source
    table = pd.read_html(data)
    df = table[1]

    browser.quit()  # 退出模拟浏览器

    company = df['股东名称'][0]
    company_split = company.split(' ')
    for i in company_split:
        if len(i) > 6:  # 不要用if '有限公司' in i，这个不太好，例如国资委不含有“有限公司 ”字样
            return i

company = '贵州茅台'
while True:    #也可以换成for i in range(n)，将n设置成一个较大的数
    try:
        company = baidu(company)  #获取company的控股股东并赋给company
        print(company)        #打印输出第一大控股股东
    except:
        break         #break语句可以跳出for或while循环

#第33行代码用baidu(company)获取当前公司的第一大控股股东，重新赋给company，然后再次循环，形成迭代爬取。当迭代到最后一家控股股东时，
#因为没有再往上的控股股东，所以try语句下的代码会报错，从而执行except语句下的break语句，跳出循环