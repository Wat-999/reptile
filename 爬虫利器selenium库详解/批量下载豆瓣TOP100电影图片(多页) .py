# #写法1
# import requests
# import re
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
#
#
# def db(page):
#     # 1.获取网页源代码
#     num = (page - 1) * 25  # 页面参数规律是（页数-1）* 25
#     url = 'https://movie.douban.com/top250?start=' + str(num)
#     res = requests.get(url, headers=headers).text
#
#     # 2.通过正则表达式获取名称title和图片网址img
#     p_title = '<img width="100" alt="(.*?)"'
#     title = re.findall(p_title, res)
#     p_img = '<img width="100" alt=".*?" src="(.*?)"'
#     img = re.findall(p_img, res)
#
#     # 3.打印图片名称，并通过requests库下载图片
#     for i in range(len(title)):
#         print(str(i + 1) + '.' + title[i])
#         print(img[i])
#         res = requests.get(img[i])  # 下面开始下载图片
#         file = open('/Users/macbookair/Desktop/简历/images/' + title[i] + '.png', 'wb')  # 需要提前创建好images文件夹！
#         file.write(res.content)
#         file.close()
#
#
# for i in range(10):  # 注意i是从0开始的序号，所以下面要写i+1页
#     db(i+1)
#     print('第' + str(i+1) + '页爬取成功！')

#写法2：用urlretrieve()函数批量下载图片
import requests
import re
from urllib.request import urlretrieve   # 也可以使用urlretrieve()批量下载
import ssl
ssl._create_default_https_context = ssl._create_unverified_context  #关闭ssl本地认证



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}


def db(page):
    # 1.获取网页源代码
    num = (page - 1) * 25  # 页面参数规律是（页数-1）* 25
    url = 'https://movie.douban.com/top250?start=' + str(num)
    res = requests.get(url, headers=headers).text

    # 2.通过正则表达式获取名称title和图片网址img
    p_title = '<img width="100" alt="(.*?)"'
    title = re.findall(p_title, res)
    p_img = '<img width="100" alt=".*?" src="(.*?)"'
    img = re.findall(p_img, res)

    # 3.打印图片名称，并通过requests库下载图片
    for i in range(len(title)):
        print(str(i + 1) + '.' + title[i])
        print(img[i])
        urlretrieve(img[i], '/Users/macbookair/Desktop/简历/images/' + title[i] + '.png')  # 需提前创建好images文件夹


for i in range(10):  # 注意i是从0开始的序号，所以下面要写i+1页
    db(i+1)
    print('第' + str(i+1) + '页爬取成功！')