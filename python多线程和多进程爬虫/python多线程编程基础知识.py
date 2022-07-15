import time
import threading  # Python自带，无需安装


def test1():
    print('任务1进行中，任务1持续3秒')
    time.sleep(3)  # 此处用time.sleep()强制休息3s
    print('任务1结束')


def test2():
    print('任务2进行中，任务2持续2秒')
    time.sleep(2)  # 此处用time.sleep()强制休息2s
    print('任务2结束')


# 常规运行代码的方法：单线程
start_time = time.time()
test1()
test2()
end_time = time.time()
total_time = end_time - start_time
print("所有任务结束，总耗时为：" + str(total_time))

# 多线程运行代码
start_time = time.time()
t1 = threading.Thread(target=test1)
t2 = threading.Thread(target=test2)
t1.start()
t2.start()
t1.join()  # 等待该子线程结束后，再执行主线程
t2.join()  # 等待该子线程结束后，再执行主线程
# 在这个案例中，先是t2执行完毕（2秒），然后还要等待t1执行完毕（3秒），他俩是同时开始执行的，所以总共是3秒后，才会执行主程序，也就是说才会执行下面的代码
end_time = time.time()
total_time = end_time - start_time
print("所有任务结束，总耗时为：" + str(total_time))
#可以看到此时test1()函数和test2()函数不再是一次执行。test1()函数启动后，先打印输出"任务1进行中，任务1持续3秒"，再开始休息3秒
#此时cpu闲置，或者说进入列IO操作时间，test2()函数便启动了。随后test2()函数依次执行自己的功能代码，
#在打印输出"任务2结束"后结束，接着test1()函数在休息完3秒后打印输出'任务1结束'并结束。整个过程耗时约3秒，比单线程的耗时(约5秒)短了不少


#补充知识点：join()函数的作用
#前面以多线程方式调用函数的代码中使用了join()韩素。在多线程任务中，join()函数的作用是让主线程必须等到子线程结束才能继续运行。
#下面用代码来帮助理解，把上面的含有join()两行代码删除
start_time = time.time()
t1 = threading.Thread(target=test1)
t2 = threading.Thread(target=test2)
t1.start()
t2.start()
# 在这个案例中，先是t2执行完毕（2秒），然后还要等待t1执行完毕（3秒），他俩是同时开始执行的，所以总共是3秒后，才会执行主程序，也就是说才会执行下面的代码
end_time = time.time()
total_time = end_time - start_time
print("所有任务结束，总耗时为：" + str(total_time))
#从打印结果可以看到，程序没有等待test1()函数和test2()函数(即线程t1和t2)结束，便打印输出来总耗时。这是因为程序开始运行时会默认启动一个主线程，
#可以将它视为线程t0。相对于主线程而言，其他定义的线程称为子线程，如下图所示
#cpu操作       IO操作        子线程1
#      cpu操作      IO操作         子线程2                                 多线程(并发)
#            cpu操作      IO操作         子线程3
#————————————————————————————————————————————————主线程t0(自动启动的)

#主线程默认不会等待子线程执行完毕，因此，当48行和49行代码用strat()函数启动子线程后，主线程会直接执行后续代码，从而过早地打印输出来总耗时
#而解决这一问题的办法非常简单，就是用strat()函数启动完所有子线程后，用join()函数让主线程等待子线程结束之后再继续执行主线程中剩下的代码。
#在这个案例中，先是线程t2执行完毕(2秒),然后还要等线程t1执行完毕(3)秒，又因为他们几乎是同时开始执行的，所以3秒后才会执行主线程中剩下的代码

#有时需求会反过来：不仅希望主线程不要等待子线程，还要求主线程一结束子线程就立即结束。此时可以使用setDaemom()守护线程函数来实现，
#不过这个函数在多线程爬虫中几乎毫无作用，简单了解即可
#最后需要注意的是，必须先用strat()函数启动所有子线程，再使用join()函数