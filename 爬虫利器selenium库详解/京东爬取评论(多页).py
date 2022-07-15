#通过Network寻找真正的评论网址

import requests
import re
headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
        "cookie" : "SINAGLOBAL=5701031797732.083.1638971150198; SUB=_2AkMW7DFkf8NxqwFRmP0QzGvkaIR1zgnEieKgsMC_JRMxHRl-yT9jqhErtRB6PWwfi8IMi4nS63fCLKIwRiYKqexEzF_Q; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFPkNiIHiOqUjBBn8.B.qFu; _s_tentry=cn.bing.com; Apache=9978275422977.867.1639488984604; UOR=,,cn.bing.com; ULV=1639488984639:4:4:1:9978275422977.867.1639488984604:1639061325022",
    }

res_all = ''  #构造一个空字符串res_all，用来汇总10页的网页源代码
for i in range(10):
    url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=10048802240823&score=5&' \
          'sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1&page=' + str(i)
    #和第一页的评价数据接口对比，发现唯一的区别就是参数page由1变成2，因此可以推算第n页对应的参数page是n。因此，用for循环语句就可以批量爬取多页评价
    #以字符串拼接的方式构造不同页面的网址(这里将参数page调整到了最后，不会影响网址请求，因为i是从0开始的，所以这里直接写str[i]

    res = requests.get(url, headers=headers).text
    res_all = res_all + res     #也可以简写成res_all += res  以字符串拼接的方式将网页源代码汇总到res_all中


p_comment = '"content":"(.*?)"'
comment = re.findall(p_comment, res_all)


for i in range(len(comment)):
    comment[i] = comment[i].replace(r'\n', '')  #这里没起作用
    print(str(i+1) + '.' + comment[i])


