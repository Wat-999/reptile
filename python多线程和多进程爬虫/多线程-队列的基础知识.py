#我们希望创建固定数量的线程，如5～10各线程，然后把多个网址分配给各个线程去爬取。要实现这样的操作，肯定需要有一个容器存放这些网址，
#而且还要能无放回地取出这些网址，也就是取出一个网址后容器里就少一个网址，这样就不会重复爬取同一个网址。
#那如何构造这个容器呢？很多读者可能会第一时间想到使用列表，但是列表是线程不安全的，因此这里引入一个新的工具——队列(queue）。队列的用法与列表类似，
#而且线程安全的，适合多线程任务。
import queue

q = queue.Queue()
# 通过put()函数写入数据
q.put(0)
q.put(1)
q.put(2)
print(q.queue)  # 输出当前队列所有数据

# 通过get()函数提取队列数据（先进先出）
keyword = q.get()
print(keyword) #因此这里先提取第一数据0

# 输出此时队列数据，此时有个数据已经被提取出去了
print(q.queue)  #此时队列的数据为1，2

# 查看此时队列是否为空，因为此时队列里还有内容deque([1, 2])，所以返回Flase
print(q.empty())

# 把队列里剩下的内容取光，然后再查看队列是否为空，这里为了快速演示，并没有把取出来的数赋值给某个变量
q.get()
q.get()
print(q.empty())

# 初步尝试
companys = ['阿里巴巴', '贵州茅台', '格力电器', '中兴通讯', '五粮液', '腾讯', '百度']
url_queue = queue.Queue()  # 创建一个空队列
for company in companys:
    url_i = 'https://www.baidu.com/s?rtt=4&tn=news&word=' + company
    url_queue.put(url_i)  #用put()函数把构造的网址写入队列url_queue中

while not url_queue.empty():  # 当队列里还有内容时，就执行下面的内容
    #其含义就是当队列里还有内容时，就一直执行下面的代码。此时url_queue.empty()的值为false，那么while not false就是while true，
    #因此会一直执行下面的代码
    url = url_queue.get()
    print(url)

# 为什么不用列表操作呢，我可以通过append()加数据，也可以通过pop()取数据，这是因为列表相对于队列Queue而言，不安全，比如它在读取和写入的时候可能会发生冲突，简单了解即可。
# 队列主要的应用场景，就是在多线程里面，其他地方用的较少，因为只有在多线程这种非常频繁的CPU处理（CPU的处理是毫秒级/纳秒级的）中，才会发生 线程冲突的 情况
# 如果只是单纯的多用户读取数据库，其实你看着好像很快，但是就算10000个人在1分钟内容访问数据库，其实对计算机来说，也还好。

'''补充知识点：Python中的线程安全问题与GIL锁（简单了解即可）'''
# import threading
# import time
# start_time = time.time()
# a = [10]  # 初始列表，里面只有1个元素10
# lock = threading.Lock()  # 加上1把线程锁
#
#
# def change():
#     global a  # 因为函数内容要对全局变量做修改，所以得通过global声明全局变量
#     for i in range(1000000):
#         with lock:
#             a[0] = a[0] + 1
#             a[0] = a[0] - 1
#
#
# # change()
# # change()
# t1 = threading.Thread(target=change)
# t2 = threading.Thread(target=change)
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(a)
# end_time = time.time()
# total_time = end_time - start_time
# print("所有任务结束，总耗时为：" + str(total_time))  # 加上锁之后，花费的时间大幅上升

