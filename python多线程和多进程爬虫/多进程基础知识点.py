import multiprocessing  #导入多进程库
import time

#print(multiprocessing.cpu_count())  #查看cpu是几核的，输出结果为8核的
#cpu是8核的，那么在这台计算机上启用的进程就尽量不要超过8个，因为一个cpu同一时间只能执行一个进程，对于多个进程也是使用时间片轮算法进行轮流调度

def test1():
    result = 0
    for i in range(20000000):
        result += i
    print(result)


def test2():
    result = 0
    for i in range(20000000):
        result += i
    print(result)


# 使用多进程运行
if __name__ == '__main__':  # 多进程必须加上这一行代码，使得在主程序中运行。而且这个在Windows系统下的Jupyter Notebook写了也没用，只能转为py格式运行
    start_time = time.time()
    t1 = multiprocessing.Process(target=test1())  #创建进程1  #注意写定义的函数不要漏掉括号(mac下）  windows不知道要不要加
    t2 = multiprocessing.Process(target=test2())  #创建进程2
    t1.start()  #启动进程1
    t2.start()
    t1.join()  #对进程1加join()函数
    t2.join()
    end_time = time.time()
    total_time = end_time - start_time
    print("[多进程方法]所有任务结束，总耗时为：" + str(total_time))


'''补充知识点：单线程和多线程的对比。
！！！注意不要同时执行3种方法的代码，
如果观察多进程的结果，那么不要管下面的代码，直接运行上面的代码即可；
如果想执行单线程或者多线程，一定要先把上面多进程的相关代码（也就是上面if __name__ == '__main__':到print()的相关代码)给注释掉再运行；
不然if __name__ == '__main__':会重复运行该代码文件里的代码，导致观察结果不太好'''
# # 常规运行代码的方法：单线程
# start_time = time.time()
# test1()
# test2()
# end_time = time.time()
# total_time = end_time - start_time
# print("[常规方法]所有任务结束，总耗时为：" + str(total_time))
#
# # 多线程，这种CPU计算密集型的任务，使用多线程会失效，下面是代码验证
# import threading
# start_time = time.time()
# t1 = threading.Thread(target=test1)
# t2 = threading.Thread(target=test2)
# t1.start()
# t2.start()
# t1.join()  # 等待该子线程结束后，再执行主线程
# t2.join()  # 等待该子线程结束后，再执行主线程
# end_time = time.time()
# total_time = end_time - start_time
# print("[多线程方法]所有任务结束，总耗时为：" + str(total_time))

