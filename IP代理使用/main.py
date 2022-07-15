'''一、功能介绍：

已实现功能：

1、爬取搜狗微信上的分类一栏的所有事件及其他的所有标题事件和加载更多，返回文章链接与标题，并存入数据库中，后续可直接根据链接下载文章。

2、根据输入内容定向爬取文章，返回链接与标题。

待实现功能：

1、根据数据库中的链接爬取公众号的所有相关文章，保存于数据库，并对所有文章分类存档。

2、实现UI界面（PyQt5），根据需要对程序打包为可执行文件。

二、运用到的知识点介绍：

selenisum（实现简单的搜狗微信主页源码获取）

代理池原理  （给定ip源，简单的判断ip是否可用）

线程池原理    （实现多线程爬取，增加爬取效率）

oo面向思想     （面向对象编程，分模块编程，增加可读性，方便后期维护）

一些常用的库    （os、time、random、requests、pymysql、queue、threading）

三、文件的结构组成及功能说明

1、main.py：该文件为程序的入口，即启动文件，功能：几个模块之间的数据传输的中转站。

2、ip_pool.py:  该文件是ip代理池文件， 功能：将给定的ip列表进行筛选，选出可用的ip方便后续请求。

2、spider_page.py:  该文件用于提取网页源码， 功能：selenisum去获取主页源码。

3、settings.py：该文件为配置文件， 功能：我们在程序启动之前可以选择爬虫的爬取方向，当然这个方向是由自己给定的。

4、is_API_Run.py:  该文件是API执行文件，功能：根据settings文件的配置输入，从而决定执行那些API函数。

5、API_Function.py:  该文件是API文件，功能：实现了各个API函数的功能实现。

6、thread_pool.py：该文件为线程池文件，功能：实现了从数据库中获取链接，去多线程的下载文章。

四、程序运行步骤代码解读

1、在我们开始之前，让我们先了解下搜狗微信的主页面：https://weixin.sogou.com/      若已了解则跳过这一步。

2、文章这里以主页中的 “搜索热词”、“编辑精选”、“热点文章”、“热门”举例演示。

3、从main文件的程序入口启动程序，首先该文件导入了一些包和编写的其他模块文件，并编写了相应的两个函数，分别是panding()函数、ip()函数，对应功能见代码注释，其他的一些模块文件在后边会有解释

文件名：main.py
————————————————
版权声明：本文为CSDN博主「*成」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/warm_man/article/details/116660501'''


'''
启动程序
'''

# 导包和导入自定义模块文件

# 自己编写的模块文件
from spider_page import __init__source
from is_API_Run import read_settings_run_func
from thread_pool import Open_Thread_Assign_Links
from ip_pool import ip_Pool

# python包
import os
import time
import random


def ip(IP_POOL):
    '''
    从IP_POOL（ip池）随机选出一个ip将其返回给主程序使用，
    :param IP_POOL: IP池
    :return: proxies ------随机的一个代理ip
    '''

    proxies = {
        "http": random.choice(IP_POOL),
    }
    return proxies


def panding(proxies):
    '''在此处实现：判断工作文件路径下的page_source目录下是否有名为当日的文件（20210511.txt）--年月日的txt文件，
    判断文件名是否符合要求（一天之内生成的）  若有则读取出来赋值page,返回给主程序使用,若没有则执行page=__init__source().html_source语句。
    获取网页源代码,再将其命名保存，并且返回给主程序使用'''

    work_path = os.getcwd()  # 获取工作路径
    html_path = os.path.join(work_path, 'page_source')
    if len(os.listdir(html_path)) > 0:  # 判断路径下是否有文件
        flag = False
        for x in os.listdir(html_path):  # 罗列出路径下所有的文件
            print("x:", x)
            if x == (time.strftime(r'%Y%m%d') + r'.txt'):  # 找出当天生成的文件
                print("x:", x)
                with open(os.path.join(html_path, x), 'r', encoding="utf-8") as f:
                    page = f.read()
                    return page

        # 没有当天的文件就创建文件并写入html源码
        page = __init__source(proxies).html_source
        with open(os.path.join(html_path, time.strftime(r'%Y%m%d') + r'.txt'), 'w', encoding="utf-8") as f:
            f.write(page)
    else:
        page = __init__source(proxies).html_source
        with open(os.path.join(html_path, time.strftime(r'%Y%m%d') + r'.txt'), 'w', encoding="utf-8") as f:
            f.write(page)

    return page  # 将源码返回给主程序使用


if __name__ == '__main__':
    IP_POOL = ip_Pool()  # 启动ip代理池   (初始化ip类，并生成代理池对象，接下来从对象中获取ip池---IP_POOL.ip_pool)

    proxies = ip(IP_POOL.ip_pool)  # 随机从ip池中拿出一个代理ip---proxies

    page = panding(proxies)  # 初始化源码 （用代理ip请求主页源码，并保存于程序工作目录下的page_source文件夹下的以年月日为名的txt文件。）

    read_settings_run_func(page, proxies)  # 读取配置文件并执行相应的API函数。

    Open_Thread_Assign_Links(proxies)  # 开启线程池下载公众号文章

