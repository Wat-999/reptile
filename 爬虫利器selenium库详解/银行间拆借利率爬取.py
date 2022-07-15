# 引入之后会用到的库
import pandas as pd
from selenium import webdriver
import time
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


# 4.1 定义第一个函数，获取上海银行间同业拆借利率（3M-1M的差值）
def libor():
    # 有界面模式成功后设置成无界面模式
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)

    url = 'http://www.shibor.org'
    browser.get(url)

    url_2 = 'http://www.shibor.org/shibor/web/html/shibor.html'  # 这个得访问过上面的网址，才能访问这个网站
    browser.get(url_2)

    data = browser.page_source

    table = pd.read_html(data)  # table是一个列表，里面有该网页里的所有表格
    df_libor = table[3]

    # 修改列名
    df_libor = df_libor[[1, 2, 4]]
    df_libor.columns = ['期限', 'Shibor(%)', '涨跌(BP)']

    M_1 = df_libor[df_libor['期限'] == '1M']['Shibor(%)'].iloc[0]  # 变量命名不可以是1M
    M_3 = df_libor[df_libor['期限'] == '3M']['Shibor(%)'].iloc[0]

    # 计算3M利率 - 1M利率
    diff = M_3 - M_1
    diff = round(diff, 3)  # 保留3位小数

    return M_3, M_1, diff


# M_3, M_1, diff = libor()
# print(M_3, M_1, diff)


# 4.2 定义第二个函数，获取兴业信托官网信息
def xingye():
    url = 'https://www.ciit.com.cn/funds-struts/fund-net-chart-table/XY0FML?from=&to=&page=1-16'  # 这个是真正的网址
    res = requests.get(url, headers=headers).text

    table = pd.read_html(res)  # table是一个列表，里面有该网页里的所有表格
    df_rate = table[0]  # 试一下就知道是table中的哪个表格了，单页的话时table[0]

    # 把第一行当作表头
    df_rate = table[0].iloc[1:]
    df_rate.columns = table[0].iloc[0]

    newest_rate = df_rate['七日年化收益率(%)'].iloc[0]

    return newest_rate


# xingye()


# 4.3 汇总代码
def summary():
    # 1.上海银行间同业拆借利率（3M-1M的差值）
    M_3, M_1, diff = libor()

    # 2.兴业的利率
    newest_rate = xingye()

    # 3.定价标准
    final_rate = float(diff) + float(newest_rate)
    final_rate = round(final_rate, 3)  # 保留3位小数

    return M_3, M_1, diff, newest_rate, final_rate


# M_3, M_1, diff, newest_rate, final_rate = summary()
# print(M_3, M_1, diff, newest_rate, final_rate)
#
# print('3月拆解利率为:' + str(M_3))
# print('1月拆解利率为:' + str(M_1))
# print('3月拆解利率 - 1月拆解利率为:' + str(diff))
# print('兴业利率:' + str(newest_rate))
# print('定价标准:' + str(final_rate))


# # 5.将数据导入数据库
import pymysql
import time

today = time.strftime("%Y-%m-%d")


def connect_db():
    return pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           password='',
                           database='monitor2',
                           charset='utf8mb4')


def save_data(M_3, M_1, diff, newest_rate, final_rate, today):
    today = time.strftime("%Y-%m-%d")  # 这个要么放在这儿，要么提前定义
    con = connect_db()
    cur = con.cursor()
    sql_str = 'INSERT INTO rate(M_3, M_1, diff, newest_rate, final_rate, date) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\', \'%s\')'
    sql_str = sql_str % (M_3, M_1, diff, newest_rate, final_rate, today)
    cur.execute(sql_str)
    con.commit()
    cur.close()
    con.close()


# M_3, M_1, diff, newest_rate, final_rate = summary()  # 运行爬虫获取数据
# try:
#     save_data(M_3, M_1, diff, newest_rate, final_rate, today)  # 导入数据库
# except:
#     print('当前日期已有数据')  # 这里我把today设置成了主键，所以不能重复

# # 6.定期爬取并存储
import schedule


def all_code():
    M_3, M_1, diff, newest_rate, final_rate = summary()  # 运行爬虫获取数据

    today = time.strftime("%Y-%m-%d")  # 其实之前函数里也写了，所以这里不写其实也可以
    try:
        save_data(M_3, M_1, diff, newest_rate, final_rate, today)  # 导入数据库
        print(today + 'success')
    except:
        print('当前日期已有数据')  # 这里我把today设置成了主键，所以不能重复


all_code()

# schedule.every().day.at("09:00").do(all_code)
# while True:
#     try:
#         schedule.run_pending()
#         time.sleep(100)
#     except:
#         print('failed')

