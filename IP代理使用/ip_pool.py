# 导包
import requests
import time
import re
import threading

# 定义测试的url链接，这里暂且选用www.baidu.com
url = 'https://www.baidu.com/'

# 定义测试的url链接www.baidu.com的请求头。
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'BIDUPSID=EAAEC44F956EC0051F3EB986A600267F; PSTM=1618841564; BD_UPN=12314753; __yjs_duid=1_fc17df5ce48c903e96c35412849fa9c21618841573172; BDUSS=F2Yn5VfmNzMFkwNjE3TzNKY0V3UVJUUW0wOUFDTVVEdU82cG9Id1lmSzEwSzFnSUFBQUFBJCQAAAAAAAAAAAEAAADrnKS8vsXOsr3wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALVDhmC1Q4ZgY0; BDUSS_BFESS=F2Yn5VfmNzMFkwNjE3TzNKY0V3UVJUUW0wOUFDTVVEdU82cG9Id1lmSzEwSzFnSUFBQUFBJCQAAAAAAAAAAAEAAADrnKS8vsXOsr3wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALVDhmC1Q4ZgY0; BAIDUID=FAD97B32882628A65DB481B25993EEA8',
    'Host': 'www.baidu.com', 'Referer': 'https', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.4071 SLBChan/15'}

# 对url网站发起请求，根据返回体的状态码判断是否请求成功，若成功则该ip可用，若不成功则ip不可用，将ip从ip池中移除。
# 那么这个ip池要保证在整个程序运行用ip皆可用

# ip供应源（ip_source）
ip_source = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=890fff42d97343ecbb39c346691044d9&orderno=YZ20225168198U2P78s&returnType=1&count=20'

# 初始化ip池为空（Ip_Pool）
Ip_Pool = []

# ip的预期存留时间M
M = 0


# ip代理池类
class ip_Pool:
    def __init__(self, ):
        self.ip_pool = []  # 初始化ip池属性，方便后续的ip池赋值。
        threading.Thread(target=self.return_ip_pool).start()  # 开启子线程动态处理ip代理池，目的：保证ip池中ip的可用性的同时，又不会影响其他程序运行。所以开辟一个子线程。
        time.sleep(6)  # 加这个等待时间，目的：给子线程足够的时间去获取ip，并填充ip池，保证返回给主程序的ip池不为空。

    def ip_yield(self):
        while True:

            while len(Ip_Pool) < 5:  # 这里的while循环语句 目的：用于检测ip池中是否始终满足个数要求
                ip = requests.get(ip_source).text  # 从ip源获取ip文本。
                if '{' in ip:  # 检测从ip源是否成功获取到ip。若未获取到ip则会返回一个包含字典样式的字符串。
                    continue
                # time.sleep(0.5)    # 可以增加等待时间，以提高获取到ip的成功率
                else:
                    ip = re.match('\S*', ip).group()  # 对获取到的ip文本简单处理，目的去除\r\n字符。
                    Ip_Pool.append(ip)  # 将ip添加到ip池中。

            # 暂停M分钟,并将Ip_Pool返回出去使用
            yield Ip_Pool
            time.sleep(M)
            print('将IP池返回给主程序使用------' + str(M) + '半分钟后对IP池进行检测是否可用--------')

            # 以下for循环是用于检测ip池中ip是否过期。
            for x in Ip_Pool:
                proxies = {'http': x}
                try:
                    if requests.get(url, proxies=proxies, headers=headers).status_code == 200:
                        # print('该ip正常，还能继续使用半分钟')
                        pass

                except Exception:
                    print('存在一个ip过期，即将从IP池中去除该ip')
                    Ip_Pool.remove(x)

    def return_ip_pool(self):
        print("ip池线程启动")
        for self.ip_pool in self.ip_yield():
            pass

