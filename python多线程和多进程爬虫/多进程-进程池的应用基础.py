
# 调用multiprocessing_on_dill包,需要安装
from multiprocessing_on_dill.dummy import Pool
import time
#MAC下
#用multiprocessing.Pool(用的是multiprocessing库）报错_pickle.PicklingError: Can't pickle <function test at 0x7fd8b83c9940>: attribute lookup test on __main__ failed
#的原因是python多进程使用的multiprocessing包默认使用pickle，
#但是pickle无法处理lambda、闭包之类的东西，把multiprocessing包换成multiprocessing_on_dill问题就解决了

def test(x):
    result = 0
    for i in range(x):
        result += i
    print('从0到' + str(x) + '的累加和为：' + str(result))


if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(processes=6)
    num = [10000000, 20000000, 30000000, 40000000, 50000000, 60000000]
    pool.map(test, num)  # 传入2个参数，函数名和函数参数列表
    end_time = time.time()
    total_time = end_time - start_time
    print("所有任务结束，总耗时为：" + str(total_time))