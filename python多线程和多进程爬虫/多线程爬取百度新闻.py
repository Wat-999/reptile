import queue
import requests
import threading
import re
import time

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

companys = ['阿里巴巴', '贵州茅台', '格力电器', '中兴通讯', '五粮液', '腾讯集团', '京东']
url_queue = queue.Queue()  # 创建一个空队列
for company in companys:
    url_i = 'https://www.baidu.com/s?rtt=4&tn=news&word=' + company
    url_queue.put(url_i)  # 将网址添加到队列中
# print(url_queue.queue)


def crawl():
    while not url_queue.empty():  # 当队列里还有内容时，就执行下面的内容
        url = url_queue.get()  # 提取队列中的网址（先进先出）
        try:  # 其实通常也不太会访问超时，但是最好还是加下吧，如果超时会执行except中的语句，不会让整个程序报错退出
            res = requests.get(url, headers=headers, timeout=10).text  # 如果怕连接超时，导致报错，可以设置try except语句
            # res = res.encode('ISO-8859-1').decode('utf-8')  # 如果爬不到内容，可能是因为反爬了，激活这两行代码查看，因为反爬后出现乱码了，还得通过5.1.3节的内容处理乱码
            # print(res)  # 如果爬取不到内容，可能是因为多次爬取太快，百度反爬了，此时可以打印下此时的网页源代码看看，解决办法是利用第8章的IP代理
        except:
            res = '访问超时'
        p_title = '<div class="result-op c-container xpath-log new-pmd".*?<div><!--s-data:{"title":"(.*?)"'
        title = re.findall(p_title, res, re.S)
        for i in range(len(title)):
            title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格
            title[i] = re.sub('<.*?>', '', title[i])
            print(str(i + 1) + '.' + title[i])


start_time = time.time()  # 起始时间

thread_list = []    #创建一个空列表用来存储线程
for i in range(10):  # 这里激活10个线程，即设置激活线程数可以自己改成1，看看单线程的时间
    thread_list.append(threading.Thread(target=crawl))   #这里因为定义的爬虫函数没有设置参数，因此这里没有写args=(参数，)
    #这里设置激活里10个线程，这10个线程会一起执行前面定义的爬虫函数crawl()，各自提取队列url_queue中的网址，直到所有网址被提取完毕，即所有爬虫任务都任务完成为止

for t in thread_list:
    t.start()  #启动线程
for t in thread_list:
    t.join() #对个线程加join()函数

end_time = time.time()  # 结束时间
total_time = end_time - start_time
print("所有任务结束，总耗时为：" + str(total_time))
#可以看到打印输出的第一条新闻标题并不是列表companys里的一家公司"阿里巴巴"的相关新闻，这是因为5个线程同时启动，那个线程先爬完并输出爬取结果是随机的

#补充知识点：多线程爬虫遇到反爬措施的解决办法
#多线程爬虫有时会被网站视为访问频率过高，从而触发网站的反爬机制，导致获取不到真正的网页源代码(需先用处理中文乱码),可以看到其中有'网络不给力，请稍后重试"
#此时的解决办法有两种：一是等待一段时间(通常几分钟)后再运行代码，二是在每次爬取时添加iP代理
