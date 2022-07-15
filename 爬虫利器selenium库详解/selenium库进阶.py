#browser.find_element_by_xpath  已弃用
#清华镜像源安装库pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple scrapy

# 1.打开及关闭网页+网页最大化
from selenium.webdriver import Chrome
Chrome = Chrome()  #声明要模拟的浏览器是谷歌浏览器
Chrome.maximize_window()  #将模拟浏览器窗口最大化
Chrome.get("https://www.baidu.com/")  #在模拟浏览器中打开指定网址
# Chrome.quit()  # 退出模拟浏览器

# 2.xpath方法来定位元素
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
Chrome = Chrome()
Chrome.get("https://www.baidu.com/")
Chrome.find_element(By.XPATH, '//*[@id="kw"]').send_keys('python') #先获取搜索框的xpth表达式，再send_keys()输入搜索内容
Chrome.find_element(By.XPATH, '//*[@id="su"]').click()  #获取百度一下的xpth的表达式，再click() 点击
Chrome.find_element(By.XPATH, '//*[@id="kw"]').clear()  #清空默认文本
# 3.css_selector方法来定位元素
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
Chrome = Chrome()
Chrome.get("https://www.baidu.com/")
Chrome.get("https://www.baidu.com/")
Chrome.find_element(By.CSS_SELECTOR, '#kw').send_keys('python')
Chrome.find_element(By.CSS_SELECTOR, '#su').click()
Chrome.find_element(By.CSS_SELECTOR, '#su').send_keys(Keys.ENTER)  #模拟键盘回车键
# 4.browser.page_source方法来获取模拟键盘鼠标点击，百度搜索python后的网页源代码
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import time
Chrome = Chrome()
Chrome.get("https://www.baidu.com/")
Chrome.find_element(By.XPATH, '//*[@id="kw"]').send_keys('python') #先获取搜索框的xpth表达式，再send_keys()输入搜索内容
Chrome.find_element(By.XPATH, '//*[@id="su"]').click()  #获取百度一下的xpth的表达式，再click() 点击
time.sleep(3)  # 因为是点击按钮后跳转，所以最好休息3秒钟再进行源代码获取,如果是直接访问网站，则通常不需要等待。
data = Chrome.page_source  #获得网页源代码
print(data)

#写法2
from selenium.webdriver.common.by import By
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://www.baidu.com/")
browser.find_element(By.XPATH, '//*[@id="kw"]').send_keys('python') #先获取搜索框的xpth表达式，再send_keys()输入搜索内容
browser.find_element(By.XPATH, '//*[@id="su"]').click()  #获取百度一下的xpth的表达式，再click() 点击
time.sleep(3)  # 因为是点击按钮后跳转，所以最好休息3秒钟再进行源代码获取,如果是直接访问网站，则通常不需要等待。
data = browser.page_source  #获得网页源代码
print(data)

# 5.browser.page_source方法来获取新浪财经股票信息
from selenium import webdriver
browser = webdriver.Chrome()
browser.get("http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml")
data = browser.page_source
print(data)

# 6.Chrome Headless无界面浏览器设置
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
Chrome = Chrome(options=chrome_options)
Chrome.get("http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml")
data = Chrome.page_source
print(data)

# # 7.补充知识点：切换子页面；切换浏览器同级页面；滚轴滚动（先暂时了解即可，之后相关案例再重点讲解）
# 此外，Selenium库以下3个知识点，虽然用的不多，但也很重要，将在之后章节逐步讲解。
#Chrome.switch_to.frame(子页面的name值)  # 这个代码要结合具体的例子来（之后会讲），暂时运行不了，就给注释掉了
# （1）切换子页面（网页中的网页），将在之后结合案例进行详细讲解；
# （2）切换浏览器同级页面，将在之后的补充知识点结合案例进行详细讲解；这里先简单举了个例子，访问百度新闻后，点击第一条新闻会新打开一个界面，目的是获取新打开页面的网页源代码
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
Chrome = Chrome()
Chrome.get("https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=阿里巴巴")
Chrome.find_element(By.XPATH, '//*[@id="1"]/div/h3/a').click()  # 模拟点击第一条新闻，会新打开一个网页

handles = Chrome.window_handles  # 获取浏览器所有窗口句柄，也即各个窗口的身份信息
# Chrome.switch_to.window(handles[0])  # 切换到最开始打开的窗口
Chrome.switch_to.window(handles[-1])  # 切换到最新（倒数第一个）打开的窗口
data = Chrome.page_source  # 这里获取到的就是新打开页面的网页源代码了
print(data)

# （3）控制滚轴滚动，将在之后节结合案例进行详细讲解。
# 方法1：滚动1个页面高度的距离（非常灵活，强烈推荐）
Chrome.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# 方法2：离最顶端向下滚动60000像素距离，通常也就是滚到最下面了
Chrome.execute_script('document.documentElement.scrollTop=60000')



