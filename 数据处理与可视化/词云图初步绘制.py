import jieba
from collections import Counter
from wordcloud import WordCloud

# 1.读取文本内容，并利用jieba.cut功能俩进行自动分词
report = open('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python/python爬虫/《Python爬虫（基础与提高）》代码汇总/第5章源代码汇总/5.爬虫数据可视化/信托行业报告.txt',
              'r', encoding='gbk').read()  # 可以自己打印下report看一下，就是文本内容 其中参数'r'表示以读取方式打开
words = jieba.cut(report)  # 将全文分割，获取到的是一个迭代器，需要通过for循环才能获取到里面的内容

# 2.通过for循环来提取words列表中大于4个字的词语
report_words = []
for word in words:
    if len(word) >= 4:
        report_words.append(word)
print(report_words)

# 3.获得打印输出高频词的出现次数
result = Counter(report_words).most_common(50)  # 取最多的50组
print(result)

# 4.绘制词云图
content = ' '.join(report_words)  # 通过join()函数把列表转换成字符串(通过' '连接列表中的元素）
wc = WordCloud(font_path='/System/Library/fonts/PingFang.ttc',  # 字体路径设置，没有设置好会乱码，无法形成词云图
               background_color='white',  # 背景颜色
               width=1000,  # 宽度
               height=600,  # 高度
               ).generate(content)  # 根据刚刚生成的content，generate成词云图
wc.to_file('词云图.png')  # 导出成png图片

