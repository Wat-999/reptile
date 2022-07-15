
import jieba  # 分词库，需要单独pip安装
from collections import Counter  # 自带的库，无需安装

# 1.读取文本内容，并利用jieba.cut功能来进行自动分词
report = open('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python/python爬虫/《Python爬虫（基础与提高）》代码汇总/第5章源代码汇总/5.爬虫数据可视化/信托行业报告.txt',
              'r', encoding='gbk').read()  # 可以自己打印下report看一下，就是文本内容 其中参数'r'表示以读取方式打开
#编程读取 .txt ，.csv 等文本文件时信息,报错解码器无法解码，直接设置encoding参数，先试常用的三种utf-8，gbk，ISO-8859-1
words = jieba.cut(report)  # 将全文分割，获取到的是一个迭代器，需要通过for循环才能获取到里面的内容

# 2.通过for循环来提取words列表中4字以上的词语
report_words = []
for word in words:
    if len(word) >= 4:  # 将4字以上的词语放入列表
        report_words.append(word)
print(report_words)

# 3.获得打印输出高频词的出现次数
result = Counter(report_words).most_common(50)  # 取最多的50组
print(result)
