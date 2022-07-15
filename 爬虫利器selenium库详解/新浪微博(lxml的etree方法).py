
#网页元素节点选取之xpath测试——python lxml的etree方法
import requests
from lxml import etree
import time
import csv

def gettime():
    # 获取当前的时间
    print("当前的时间是：", time.strftime("%Y-%m-%d %H:%M:%S"))
    pass

def save(name, hot):
    lsname = []
    for i in range(0, len(name)):
        lsname.append([name[i], hot[i]])
    with open("hot.csv", "w", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lsname)

if __name__ == "__main__":

    gettime()

    # 确认目标的 url
    _url = "https://s.weibo.com/top/summary"

    # 手动构造请求的参数
    _headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
        "cookie" : "SINAGLOBAL=5701031797732.083.1638971150198; SUB=_2AkMW7DFkf8NxqwFRmP0QzGvkaIR1zgnEieKgsMC_JRMxHRl-yT9jqhErtRB6PWwfi8IMi4nS63fCLKIwRiYKqexEzF_Q; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFPkNiIHiOqUjBBn8.B.qFu; _s_tentry=cn.bing.com; Apache=9978275422977.867.1639488984604; UOR=,,cn.bing.com; ULV=1639488984639:4:4:1:9978275422977.867.1639488984604:1639061325022",
        # "Referer": "https://www.baidu.com/link?url=j4BATujs6r1tDJgq8AqwTKYFP94_YcXPDXrDW9XKN2wmO0CyWck18MN0ES1bM5gX&wd=&eqid=fdbaa254000e24100000000261b05229"
    }

    # 发送请求
    _response = requests.get(_url, headers = _headers)
    _data = _response.text
    # print(data_)

    # 提取数据
    html_obj = etree.HTML(_data)

    # 置顶微博： 1.名称 2.url 链接
    name_top = html_obj.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr[1]/td[2]/a/text()')[0]
    #xpath=//*[@id="pl_top_realtimehot"]/table/tbody/tr[1]/td[2]/a
    #a/text()表示a元素节点下子节点中的文本节点

    url_top = html_obj.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr[1]/td[2]/a/@href')[0]
    #a/@href表示a元素节点下子节点中href的属性节点
    url_top = "https://s.weibo.com/" + url_top

    #print(f'置顶微博：{name_top}，链接地址：{url_top}')

    # 热搜榜微博：1.名称 2.序号 3.热度
    # 热搜榜名称
    name_list = html_obj.xpath('//td/span/preceding-sibling::a/text()')
    #xpath的选取方法：从节点中选取元素所在的在的节点再选取文本或属性
    #/表示从根节点选取    //表示从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置
    #.表示选取当前节点       ..表示选取当前节点的父节点   @表示选取属性
    #获取兄节点：preceding-sibling::
    print(len(name_list))
    print(name_list)
    # 热搜榜热度
    hot_list = html_obj.xpath('//td/span/text()')
    print(len(hot_list))
    print(hot_list)
    save(name_list, hot_list)



