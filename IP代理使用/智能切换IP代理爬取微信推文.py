# 2.4 添加IP代理爬取微信推文 by 王宇韬(微信；18014699850) 网址：https://www.huaxiaozhi.com
# ===========================================================================================
import requests
import re
import time
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}


def weixin(company):
    # 1.获取网页源代码
    url = 'https://weixin.sogou.com/weixin?type=2&query=' + company
    #url = 'https://httpbin.org/get'  # 这个可以用来查看IP代理是否成功
    res = requests.get(url, headers=headers, timeout=10, proxies=proxies).text  # 这里新加了一个proxies=proxies
    try:
        res = res.encode('ISO-8859-1').decode('utf-8')  # 方法3
    except:
        try:
            res = res.encode('ISO-8859-1').decode('gbk')  # 方法2
        except:
            res = res  # 方法1
    # print(res)

    # 2.编写正则表达式
    p_title = 'uigs="article_title_.*?">(.*?)</a>'  # 标题
    p_source = 'uigs="article_account_.*?">(.*?)</a>'  # 新闻来源
    p_date = 'timeConvert\(\'(.*?)\'\)'  # 日期
    p_href = '<div class="txt-box">.*?<h3>.*?<a target="_blank" href="(.*?)"'  # 网址
    title = re.findall(p_title, res)
    source = re.findall(p_source, res)
    date = re.findall(p_date, res)
    href = re.findall(p_href, res, re.S)

    # 3.清洗并打印数据
    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        title[i] = re.sub('&.*?;', '', title[i])
        timestamp = int(date[i])
        timeArray = time.localtime(timestamp)
        date[i] = time.strftime("%Y-%m-%d", timeArray)
        href[i] = 'https://weixin.sogou.com' + href[i]
        print(str(i+1) + '.' + title[i] + ' + ' + source[i] + ' + ' + date[i])
        print(href[i])

    return res  # 返回网页源代码，用来之后判断是否为验证码页


def changeip():
    proxy = requests.get('http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=890fff42d97343ecbb39c346691044d9&orderno=YZ20225168198U2P78s&returnType=1&count=10').text  # 讯代理官网：http://www.xdaili.cn/buyproxy
    proxy = proxy.strip()
    print('提取IP为：' + proxy)
    proxies = {"http": "http://" + proxy, "https": "https://" + proxy}
    time.sleep(10)
    return proxies


proxies = changeip()

# 下面开始进行智能IP切换
companys = ['华能信托', '阿里巴巴', '万科集团']
for i in companys:
    try:
        res = weixin(i)
        while '验证码' in res:  # while else类似 if else，不过可以一直循环，直到不再满足while中的条件为止
            print('原代理IP失效，开始切换IP')
            proxies = changeip()
            res = weixin(i)
        else:
            print(i + '该公司微信推文爬取成功')

    except:
        print(i + '该公司微信推文爬取失败')

