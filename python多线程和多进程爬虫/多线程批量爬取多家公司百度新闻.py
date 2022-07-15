# 如果函数中有参数，多线程的调用方式 - 爬虫初步实战
import time
import requests
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}


def test(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=4&word=' + company
    res = requests.get(url, headers=headers).text
    print(len(res))  # 可以把这行代码，换成3.1节获取源代码/解析和打印标题相关代码，这里主要为了快速演示


# 用多线程
companys = ['阿里巴巴', '华能信托', '京东', '腾讯', '京东']
start_time = time.time()

thread_list = []  # 创建一个空列表，用来存储每一个线程，这个方法下一小节会优化下，因为你如果有1000个网站，不应该创建1000个线程，激活线程需要资源的
for i in range(len(companys)):
    t = threading.Thread(target=test, args=(companys[i],)) #遍历公司名称列表，为每一家公司创建独立的线程
    #args=(companys[i],)传入公司名称
    thread_list.append(t) #添加线程

for i in thread_list:  #注意不能把启动各个线程与对每个线程应用join()函数写在一个循环里面
    i.start()  #启动各个线程

for i in thread_list:
    i.join()  #对每个线程应用join()函数

end_time = time.time()
total_time = end_time - start_time
print("所有任务结束，总耗时为：" + str(total_time))

'''补充知识点：有的时候网络请求会连接超时，导致一直卡着不动。
此时可以设置timeout参数，然后通过try except避免报错（如果不设置try except，出现超时后程序会提示报错而使得程序终止）'''
# def test(company):
#     url = 'https://www.baidu.com/s?tn=news&rtt=4&word=' + company
#     try:
#         res = requests.get(url, headers=headers, timeout=10).text
#         print(len(res))
#     except:
#         res = '访问超时'

