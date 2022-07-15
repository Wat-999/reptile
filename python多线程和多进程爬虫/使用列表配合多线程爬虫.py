# 这个代码没有写到书上，因为这个是用列表list而不是队列Queue实现的，因为append()和pop()操作属于原子操作（即不是拆分成多个步骤的操作，例如a[0]=a[0]+1），所以不会产生线程冲突
# 所以其实对于本案例来说，使用列表list还是队列Queue，笔者感觉都可以，不过还是建议在多线程任务中使用队列Queue（因为大家都是这么用的嘛）
import queue
import requests
import threading
import re
import time

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

companys = ['阿里巴巴', '贵州茅台', '格力电器', '中兴通讯', '五粮液', '京东', '腾讯集团']
url_list = []  # 这里主要演示下其实用列表也是可以的，因为append()和pop()操作属于原子操作（即不是拆分成多个步骤的操作，例如a[0]=a[0]+1），所以不会产生线程冲突
for company in companys:
    url_i = 'https://www.baidu.com/s?rtt=4&tn=news&word=' + company
    url_list.append(url_i)  # 通过append()函数添加内容
# print(url_list)


def crawl():
    while len(url_list) != 0:  # 通过len(url_list)网址列表长度不等于0判断还应该执行下面的代码
        url = url_list.pop()  # 通过pop()函数提取内容 后进后出
        try:  # 其实通常也不太会访问超时，但是最好还是加下吧，如果超时会执行except中的语句，不会让整个程序报错退出
            res = requests.get(url, headers=headers, timeout=10).text  # 如果怕连接超时，导致报错，可以设置try except语句
        except:
            res = '访问超时'
        p_title = '<div class="result-op c-container xpath-log new-pmd".*?<div><!--s-data:{"title":"(.*?)"'
        title = re.findall(p_title, res, re.S)
        for i in range(len(title)):
            title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格
            title[i] = re.sub('<.*?>', '', title[i])
            print(str(i + 1) + '.' + title[i])


start_time = time.time()  # 起始时间

thread_list = []
for i in range(5):  # 这里激活5个线程
    thread_list.append(threading.Thread(target=crawl))

for t in thread_list:
    t.start()
for t in thread_list:
    t.join()

end_time = time.time()  # 结束时间
total_time = end_time - start_time
print("所有任务结束，总耗时为：" + str(total_time))

