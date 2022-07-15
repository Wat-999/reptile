# 如果函数中有参数，多线程的调用方式
import threading
import time


def test1(x):
    print('任务进行中，此时参数为' + str(x))  # 这边使用str()函数是怕有的人会传入数字，这样反正都可以转为字符串就不怕字符串拼接数字导致报错
    time.sleep(3)  # 此处用time.sleep()强制休息3s
    print('任务1结束')


def test2(x):  # 最好还是改成2个函数吧
    print('任务进行中，此时参数为' + str(x))  # 这边使用str()函数是怕有的人会传入数字，这样反正都可以转为字符串就不怕字符串拼接数字导致报错
    time.sleep(2)  # 此处用time.sleep()强制休息3s
    print('任务2结束')


start_time = time.time()
t1 = threading.Thread(target=test1, args=('x1', ))  # args必须是个元组（类似列表的一个东西），如果只有一个参数，一定要加一个逗号，否则就不是一个tuple元组
t2 = threading.Thread(target=test2, args=('x2', ))  # 如果是传入多个参数，就不用考虑上面那个问题了
t1.start()
t2.start()
t1.join()
t2.join()
end_time = time.time()
total_time = end_time - start_time
print('所有任务结束，总耗时为：' + str(total_time))

