# 2.3 添加IP代理爬取微信推文
import requests
import re
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


def weixin(company):
    # 1.获取网页源代码
    url = 'https://weixin.sogou.com/weixin?type=2&query=' + company
    # url = 'https://httpbin.org/get'  # 这个可以用来查看IP代理是否成功
    res = requests.get(url, headers=headers, timeout=10, proxies=proxies).text  # 这里新加了一个proxies=proxies
    try:  # 因为出现验证码的界面直接requests请求会出现乱码，所以需要加上下面的处理乱码的方法
        res = res.encode('ISO-8859-1').decode('utf-8')  # 方法3
    except:
        try:
            res = res.encode('ISO-8859-1').decode('gbk')  # 方法2
        except:
            res = res  # 方法1
    # print(res)  # 如果把上面的try except语句注释掉，如果IP是无效的，就能看到验证码界面是乱码的内容

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


# 新增的IP代理内容
proxy = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD2022637793ns7bwc/ef58b383d5b411ec874b7cd30ad3a9d6?returnType=1').text  # 讯代理官网：http://www.xdaili.cn/buyproxy
proxy = proxy.strip()
print('提取IP为：' + proxy)
proxies = {"http": "http://" + proxy, "https": "https://" + proxy}

companys = ['华能信托', '阿里巴巴', '万科集团']
for i in companys:
    try:
        weixin(i)
        print(i + '该公司微信推文爬取成功')  # 但是如果只是打印这一句话，而没有打印具体内容，说明IP也是失效的。此时可以打印res会发现并没有爬取所需内容
    except:
        print('连接超时，爬取失败')



