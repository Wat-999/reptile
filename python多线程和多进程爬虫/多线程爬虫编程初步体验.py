import time
import requests
import threading

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}


def test1():  # 对于爬虫来说，大部分操作是IO操作（请求网页/等待网页相应（占据了爬虫的大量时间）等），不涉及CPU计算密集型任务（如果爬虫任务里有解析网页的话，是属于CPU操作的），所以可以采用多线程
    url = 'https://www.baidu.com/s?tn=news&rtt=4&word=阿里巴巴'
    res = requests.get(url, headers=headers).text
    print(len(res))  # 可以把这行代码，换成3.1节获取源代码/解析和打印标题相关代码


def test2():
    url = 'https://www.baidu.com/s?tn=news&rtt=4&&word=贵州茅台'
    res = requests.get(url, headers=headers).text
    print(len(res))  # 可以把这行代码，换成3.1节获取源代码/解析和打印标题相关代码


# 先不用多线程
start_time = time.time()
test1()
test2()
end_time = time.time()
total_time = end_time - start_time
print("所有任务结束，总耗时为：" + str(total_time))

# 用多线程
start_time = time.time()
t1 = threading.Thread(target=test1)
t2 = threading.Thread(target=test2)
t1.start()
t2.start()
t1.join()
t2.join()
end_time = time.time()
total_time = end_time - start_time
print("所有任务结束，总耗时为：" + str(total_time))


