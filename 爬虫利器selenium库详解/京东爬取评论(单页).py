#通过Network寻找真正的评论网址

import requests
import re
headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
        "cookie" : "SINAGLOBAL=5701031797732.083.1638971150198; SUB=_2AkMW7DFkf8NxqwFRmP0QzGvkaIR1zgnEieKgsMC_JRMxHRl-yT9jqhErtRB6PWwfi8IMi4nS63fCLKIwRiYKqexEzF_Q; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFPkNiIHiOqUjBBn8.B.qFu; _s_tentry=cn.bing.com; Apache=9978275422977.867.1639488984604; UOR=,,cn.bing.com; ULV=1639488984639:4:4:1:9978275422977.867.1639488984604:1639061325022",
    }
url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=10048802240823&score=5&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
res = requests.get(url, headers=headers).text
p_comment = '"content":"(.*?)"'
comment = re.findall(p_comment, res)
for i in range(len(comment)):
    comment[i] = comment[i].replace(r'\n', '')  #这里没起作用
    print(str(i+1) + '.' + comment[i])