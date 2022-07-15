
# 导包
from multiprocessing import cpu_count
import threading
import requests
import queue
import pymysql
import time

'''
pymysql创建一个coon数据库对象，将数据库中的重复链接去重（变唯一），把所有的链接拿出来放到队列中去（需要定义队列对象--初始化队列对象）
从队列中拿出数据分给线程去处理，注意:拿出数据的这个动作它是唯一的（就是只能每次一个线程去拿----加锁--锁定只能一个线程拿---线程锁）
编写线程函数--每个线程函数内容皆一样（都是去下载html页面，用到的是requests库），将数据放到数据库中-建表--方便后面数据清洗
'''

















class Open_Thread_Assign_Links():  # 开启线程，分配链接

    def __init__(self ,proxies):
        # 请求头
        self.headers = {'authority': 'weixin.sogou.com', 'method': 'GET', 'path': '/', 'scheme': 'https',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9',
                        'cache-control': 'max-age=0',
                        'cookie': 'ABTEST=7|1619743404|v1; IPLOC=CN3205; SUID=5E9A50754018960A00000000608B52AC; SUID=5E9A5075AF21B00A00000000608B52AC; weixinIndexVisited=1; SUV=0087AD4475509A5E608B52ADF7A81201; SNUID=CD8A73542124E19CE9C1C01321869CD8; JSESSIONID=aaaUz7AAKRNv6gHXIfJGx',
                        'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none',
                        'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.4071 SLBChan/15'}

        # 创建锁对象
        self.lock = threading.Lock()

        # 确定线程数
        self.Mul_Num()

        # 代理
        self.proxie s =proxies

        # 创建队列
        self.q = queue.Queue(500)

        # 从数据库中取出url数据
        self.url_tuple = self.get()

        # 将链接压进队列
        self.Push_Element_Queue(self.url_tuple)

        # 启动线程处理队列
        self.Run_thread()



    def get(self):  # 从数据库中取出url数据                          #便于初始化类时从数据库中拿出数据，也方便后续界面用户发起的请求
        coon = pymysql.connect(user='root', password='clly0528', db='gc')
        cur = coon.cursor()
        cur.execute('select * from urls')
        urls_list = cur.fetchall()
        # print("*:",urls_list)
        return urls_list



    def Push_Element_Queue(self, urls_list):
        for tuple_x in urls_list:
            self.q.put(tuple_x[1])  # 将链接压进队列
            # print("q:",self.q)




    def Run_thread(self):
        cu t =0
        for thread_id in range(self.mul_num):
            cu t+ =1
            threading.Thread(target=self.spider ,args=(self.q ,cut)).start()
            print("已成功开启%d个线程" % self.mul_num)




    # 线程函数
    def spider(self ,lq ,cut):
        print("开启线程 %d ...." % cut)
        while True:
            while lq.empty:
                # 加锁
                self.lock.acquire()

                # 保证这个动作单一，同一时间只能由一个线程主管
                url = lq.get(block=True, timeout=None)

                # 解锁
                self.lock.release()

                # 这里获取到返回体，将返回体通过yield关键字传递给数据处理类。。
                print("下载文章...")
                respones e =requests.get(url=url ,headers=self.headers ,proxies=self.proxies)

                # 文章内容写入磁盘
                Generate_file(responese)

    # 确定开启几个线程
    def Mul_Num(self):
        # x: cpu实际运行时间   y: 线程等待时间
        N = cpu_count()
        x = 1
        y = 5
        self.mul_num = int(N * (x + y) / x)

    # 将下载后的文章写入磁盘html_page中
def Generate_file(responese):
    print("文章写入文件夹")
    with open(r'C:\Users\Windows_pycharm\Desktop\G\图书管理系统\微信公众号爬取\html_page ' +'\\ ' +time.strftime
            ('%Y%m%d%H%M%S') + '.txt' ,'w' ,encoding='utf-8') as f:
        f.write(responese.text)






















