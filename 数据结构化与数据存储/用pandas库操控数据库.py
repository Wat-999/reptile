#连接数据库
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/sys')
#参数字符串中各部分的含义：数据库类型+数据库驱动程序：//数据库用户名：密码@数据库服务器IP地址：端口/数据库名

#2读取数据
# import pandas as pd
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/sys')
# sql = 'SELECT * FROM article'
# df = pd.read_sql_query(sql, engine)
# print(df.head())

#3写入数据
#用pandas库的to_sql()函数可以快速将数据写入数据库
#import pandas as pd
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/sys')
# df = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python/python爬虫/《Python爬虫（基础与提高）》代码汇总/第6章源代码汇总/8.Python连接数据库/百度新闻-带评分.xlsx')
# #df = df.astype('str')  #如果有报错数据格式的问题，即用astype()函数来处理
# df.to_sql('article', engine, index=False, if_exists='append')
#第一个参数为要写入的表名，没有会自动创建，有的话会追加注意表头一致
#第二个参数为数据库连接
#第三个参数为忽略行索引
#第四个参数为如果数据表已存在则继续添加
#其文本数据的默认格式为text长文本格式，与之前使用的varchar常规文本格式区别不大
#if_exists一个属性为replace，即删除原有数据，再重新写入数据，注意但是会改变表结构和数据类型
#如果想删除原有数据，又要保持原有的表结构和类型，解决方案就是先执行sql语句删除表数据，再用'append'属性进行追加写入

#在sql语句中传入动态参数
#有时sql语句中的参数是动态变化的，例如，要在数据表中'abjk'中 提取今天的数据，而今天的日期是动态变化的，此时就要传入动态参数的方式编写sql语句
# import time
# import pandas as pd
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/sys')
# today = time.strftime('%Y-%m_%d')  #今天的日期，字符串格式
# sql = 'SELECT * FROM abjk WHERE 日期 = %(date)s'  #用于在数据表abjk中提取今天的数据，其中date是一个动态参数(可已换成其他变量名，只要与下面一行代码中的变量名一致即可）
# #%()s表示以字符串格式传入
# df_old = pd.read_sql_query(sql, engine, params={'date': today})
# #params代表要为sql语句传入的动态参数，其值包含一个键值对应的字典，其中的键'date'就是37行中定义的动态参数，而键对应的值today则是36行中定义的日期变量
# #如果需要，可以传入多个动态参数，例如传入两个动态参数写法为params={'date'：today， 'score'：today_score}



#数据去重的另一种思路
#用pandas库可以将数据快速去重并写入数据库。假设df为刚爬取的新闻数据，df_old为数据库里存储的新闻数据，df和df_old有重复的内容，现在要把在df中
#而不在df_old中的数据(也就是与数据库中已有数据不重复的新闻数据)写入数据库，那么可以通过如下代码进行去重(这里认为新闻标题重复就是重复内容)
#df_new = df[~df['标题'].isin(df_old['标题'])]
#这里有两个新知识点：一个是isin()函数：该函数接受一个列表或数组(如上面的df_old['标题']作为参数，判断目标列(如上面的df['标题']中的元素是否在列表中，
#如果在则返回True,否则返回false。因此代码的含义就是筛选同时出现在df['标题']列和df_old['标题']列中的内容
#理解列isin()函数，再来讲解"～"符号，它的作用是取反，也就是取选中数据之外的数据，因此df[~df['标题'].isin(df_old['标题'])]就表示
#选择df['标题']列中独有的内容(也就是没有出现在df_old['标题']列中的内容，这样便去除列df中与df_old重复的内容

#示例
import pandas as pd
df = pd.DataFrame({'标题': ['标题1', '标题2'], '日期': ['日期1', '日期2']})
df_old = pd.DataFrame({'标题': ['标题2', '标题3'], '日期': ['日期2', '日期3']})
df_new = df[~df['标题'].isin(df_old['标题'])]
df_new1 = df[df['标题'].isin(df_old['标题'])]
print(df_new)  #此时df_new结果显示，成功的筛选出df中独有的内容，即就是去除列与df_old中相同的内容
print(df_new1) #此时df_new结果显示，成功的筛选出df与df_old相同的内容，即两者之间的交集
#成功去重后，就可以用to_sql()函数将处理好的df_new写入数据库了

#取两个表格的非重复值
#前面讲解的数据去重是保留df中独有的内容，如果想同时保留df和df_old中独有内容也就是它们的非重复值
import pandas as pd
df_q = pd.DataFrame({'标题': ['标题2', '标题3'], '日期': ['日期2', '日期3']})
df_olds = pd.DataFrame({'标题': ['标题3', '标题4'], '日期': ['日期3', '日期4']})
df_newd = df_q.append(df_olds)   #也可以写成pa.concat([df, df_old])
df_newd = df_newd.drop_duplicates(keep=False)  #数据去重，keep=false表示删除所有重复行
#其中keep可取的值有：'first'：默认值，表示保留首次出现的重复行，删除后面的重复行
#'last'：表示保留最后一次出现的重复行，删除前面的重复行
#'false'：表示删除所有重复行
print(df_newd)

#模糊筛选
#用用pandas库对数据进行模糊筛选，可以使用contains()函数，其功能是筛选目标劣种含有某一关键词的行。基本语法格式为：df[df['列名'].str.contains(关键词)]
#其中先用str属性将内容转换为字符串，然后才能使用contains()函数进行筛选(因为非字符串格式数据不能和字符串格式数据比较)
#示例
import pandas as pd

df = pd.DataFrame([['liver', 'E', 89, 21, 24, 64],
                   ['Arry', 'C', 36, 37, 37, 57],
                   ['Ack', 'A', 57, 60, 18, 84],
                   ['Eorge', 'C', 93, 96, 71, 78],
                   ['Oah', 'D', 65, 49, 61, 86]
                   ],
                  columns=['name', 'team', 'Q1', 'Q2', 'Q3', 'Q4'])

# 名字包含A字母
res1 = df.loc[df.name.str.contains('A')]  ##data.loc['a']取索引为'a'的行
print(res1)
z = df[df.name.str.contains('A')]
print(z)
# 名字包含A字母或E字母
res2 = df.loc[df.name.str.contains('A|E')]
# 忽略大小写
import re

res3 = df.loc[df.name.str.contains('A|E', flags=re.IGNORECASE)]
# 包含数字
res4 = df.loc[df.name.str.contains('\d')]

