'"爬虫任务涉及的操作大多是IO操作，所以多进程与多线程爬虫多效果类似'
from multiprocessing_on_dill.dummy import Pool
import time
import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}


def baidu(company):  # 百度新闻爬虫相关知识点可参考3.1节
    url = 'https://www.baidu.com/s?tn=news&rtt=4&word=' + company  # rtt=4即是按时间排序，默认为1按焦点排序
    res = requests.get(url, headers=headers).text  # 这里其实最好也像之前的7.2节的代码一样，加上timeout参数，并设置下try except语句
    p_title = '<div class="result-op c-container xpath-log new-pmd".*?<div><!--s-data:{"title":"(.*?)"'
    title = re.findall(p_title, res, re.S)
    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        print(str(i + 1) + '.' + title[i])


if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(processes=7)  #设置进程数
    companys = ['阿里巴巴', '贵州茅台', '格力电器', '中兴通讯', '五粮液', '腾讯', '京东']
    pool.map(baidu, companys)  # 传入2个参数，函数名和函数参数列表
    end_time = time.time()
    total_time = end_time - start_time
    print("所有任务结束，总耗时为：" + str(total_time))

