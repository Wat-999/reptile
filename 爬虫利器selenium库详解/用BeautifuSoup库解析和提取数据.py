#一个快速验证网页是否被动态渲染的方法是：用右键查看源代码，如果看到的网页源代码内容很少，也不包含用开发者工具能看到的信息，就可以判定用开发者工具
#看到的网页源代码是动态渲染的结果。例如，用右键快捷菜单查看上证综合指数页面的网页源代码，按快捷键cmd+f打开搜索框，1搜索页面中看到的指数数值
#2会发现搜索不到，即说明这个页面是动态渲染出来的

#解析特定标签的网页元素
from bs4 import BeautifulSoup
res = '''
<html>
    <body>
        <h1 class="title">华能信托是家好公司</h1>
        <h1 class="title">上海交大是所好学校</h1>
        <a href="https://www.baidu.com/" id="source">百度新闻</a> 
    </body>
</html>
'''
soup = BeautifulSoup(res, 'html.parser')  # 激活BS库，使用html解析器，res则是之前创建好的网页源代码，并将解析器命名为soup
title = soup.select('h1') #用select()函数选取所有<h1>标签，传入的参数为标签名
print(title)

source = soup.select('a')  #选取所有<a>便签
print(source)

#如果想进一步提取标签中的文本内容，则需要遍历各个标签，然后通过text属性提取文本内容
for i in title:
    print(i.text)


#通过text属性提取文本内容的一个好处是它只提取文本，会自动忽略可能存在的<em>或</em>等标签，因而无须再对提取结果做数据清洗
title_all = []  # 创建空列表，用来存储文本
for i in title:
    title_all.append(i.text)  # 通过append()函数添加文本内容i.text
print(title_all)

#解析特定属性的网页元素
#本例中，所有<h1>标签的class属性都为"title"
title = soup.select('.title')
print(title)
#和解析特定标签的网页元素不同，这里在select()函数中输入的参数不是标签名，而是class属性的值，而且在属性值前需要加上"."，用于声明寻找的是class属性

#可以看到所有class属性为title的标签都被选取来，然后用text属性提取标签中的文本内容
for i in title:
    print(i.text)

#同理，如果想选取特定ID属性的标签
source = soup.select('#source')
print(source)
#与根据class属性选取标签唯一的区别是，在属性值前用"#"号来声明寻找的是id属性

#补充知识点：select()函数的多层次筛选
#网页源代码中的标签通常是层层嵌套的关系，在如下缩示例代码中，第3行的<h1>标签就是包含在第2～4行的<div>标签中
res = '''
<div class="result1">
    <h1 class="title">华能信托是家好公司</h1>
</div>
<div class="result2">
    <h1 class="title">华能信托是家好公司</h1>
</div>
'''

#如果只想提取class属性为"result1"的<div>标签里的标题信息，就要利用select()函数的多层次筛选功能
soup = BeautifulSoup(res, 'html.parser')  # 激活BS库，使用html解析器
title = soup.select('.result1 h1')  # 核心代码，多层次筛选
#title = soup.select('.result1.title')   #等同上面
print(title)
#其核心为第58行代码，通过在select()函数中连续传入多个层级的筛选条件，实现多层次筛选
#该行代码也可以写成title = soup.select('.result1.title')

#提取<a>标签中的网址
res = '''
<html>
    <body>
        <h1 class="title">华能信托是家好公司</h1>
        <h1 class="title">上海交大是所好学校</h1>
        <a href="https://www.baidu.com/" id="source">百度新闻</a> 
    </body>
</html>
'''
source = soup.select('a')
for i in source:
    print(i['href'])

#知识点：
#根据标签名选取标签：soup.select('h1')              提取标签的文本内容： i.text
#根据class属性选取标签： soup.select('.title')      提取<a>标签中的网址： i['href']
#根据id属性选取标签： soup.select('#source')