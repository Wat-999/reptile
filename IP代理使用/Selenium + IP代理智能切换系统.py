from selenium import webdriver
import re
import time
import requests


def weixin(company):
    # 1.使用代理并获取网页源代码
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=' + proxy)
    browser = webdriver.Chrome(options=chrome_options)
    url = 'https://weixin.sogou.com/weixin?type=2&query=' + company
    browser.get(url)
    data = browser.page_source
    # print(data)

    # 2.编写正则表达式
    p_title = 'uigs="article_title_.*?">(.*?)</a>'  # 标题
    p_source = 'uigs="article_account_.*?">(.*?)</a>'  # 新闻来源
    p_date = 'timeConvert\(\'(.*?)\'\)'  # 日期
    p_href = '<div class="txt-box">\n<h3>\n<a target="_blank" href="(.*?)"'  # 网址  其中\n表示换行，也可以用.*?代替换行
    title = re.findall(p_title, data)
    source = re.findall(p_source, data)
    date = re.findall(p_date, data)
    href = re.findall(p_href, data, re.S)

    # 3.清洗并打印数据
    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])  # 清理标题中的"<em>、</em>、只要是<任意内容>"
        title[i] = re.sub('&.*?;', '', title[i])  # 清洗"$.*?:"格式的内容
        timestamp = int(date[i])  # 用正则提取出来的是字符串，因此用int()函数将其转为数字
        timeArray = time.localtime(timestamp)  # 将时间戳转换为常规格式的日期
        date[i] = time.strftime("%Y-%m-%d", timeArray)  # 指定日期格式
        href[i] = 'https://weixin.sogou.com' + href[i]
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + ' ' + source[i] + ')')
        print(href[i])

    return data  #将获取的网页源代码设置为函数的返回值


def changeip():
    proxy = requests.get('https://api.xiaoxiangdaili.com/ip/get?appKey=852915282384408576&appSecret=d3FAyeaL&cnt=&wt=text').text
    proxy = proxy.strip()
    print('提取IP为：' + proxy)
    time.sleep(5)
    return proxy


proxy = changeip()  # 获取一个IP地址

# 下面开始进行智能IP切换
companys = ['华能信托', '阿里巴巴', '万科集团']
for j in companys:
    try:
        data = weixin(j)
        while '验证码' in data:  # 判断是否为验证码页
            browser.quit()  # 如果是验证码页，退出目前的网页
            print('原代理IP失效，开始切换IP')
            proxies = changeip()
            data = weixin(j)
        else:
            print(j + '该公司微信推文爬取成功')

    except:
        print(j + '该公司微信推文爬取失败')
#browser.quit()  # 退出模拟的网页

