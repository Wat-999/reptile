
# 导包
import requests
from bs4 import BeautifulSoup
import pymysql


# 后面发起请求会用到的请求头和请求url
url = 'https://weixin.sogou.com/'  # 搜狗微信的入口url链接
headers = {'authority': 'weixin.sogou.com', 'method': 'GET', 'path': '/', 'scheme': 'https',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'cache-control': 'max-age=0',
           'cookie': 'ABTEST=7|1619743404|v1; IPLOC=CN3205; SUID=5E9A50754018960A00000000608B52AC; SUID=5E9A5075AF21B00A00000000608B52AC; weixinIndexVisited=1; SUV=0087AD4475509A5E608B52ADF7A81201; SNUID=CD8A73542124E19CE9C1C01321869CD8; JSESSIONID=aaaUz7AAKRNv6gHXIfJGx',
           'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.4071 SLBChan/15'}




class Functions():
    def __init__(self, page, proxies):
        # 代理
        self.proxies = proxies

        # 搜狗微信主页的网页源码
        self.page = page

        # bs4初始化网页源码
        self.soup = BeautifulSoup(self.page, 'lxml')

        # 连接mysql数据库，返回一个数据库对象
        self.coon = pymysql.connect(user='root', password='clly0528', db='gc')

        # 创建游标对象，方便后续执行sql语句操作
        self.cur = self.coon.cursor()

        # 删除已存在的同名的数据表
        self.clear_database()

    def clear_database(self):
        self.cur.execute("show tables like 'urls'")
        if len(self.cur.fetchall()) == 0:
            print("创建表")
            # 创建表
            self.cur.execute('''create table urls(id int not NULL auto_increment,
                                                      href varchar(500) not NULL,
                                                      title varchar(500) not NULL,
                                                      primary key (id)
                                                      );''')
        else:

            # 删除表
            self.cur.execute("drop table urls")
            self.coon.commit()

            # 创建表
            print(30 * '-' + "删除原表，创建新表！" + 30 * '-')
            self.cur.execute('''create table urls(id int  auto_increment primary key,
                                                      href varchar(500) not NULL,
                                                      title varchar(500) not NULL
                                                      );''')
        # 提交保存
        self.coon.commit()

    # ***********************************************************************************************************************
    def Search_hot_words(self):  # 搜索热词
        for tag in self.soup.select('#topwords > li > a'):  # 罗列出每个tga标签对象的href属性与title属性
            sql = r"insert into urls(href,title) value(" + "'" + tag.attrs['href'] + "'" + ',' + "'" + tag.attrs[
                'title'] + "'" + ")"
            print("搜索热词sql: ", sql)
            self.cur.execute(sql)
            self.coon.commit()

    def Editor_s_selection(self):  # 编辑精选
        p_soup_list = self.soup.select(".aside >p")
        for p_soup in p_soup_list:
            if p_soup.get_text() == "编辑精选":
                a_soup = p_soup.find_next("ul").select('li >.txt-box > .p1 >a')
                for tag in a_soup:
                    sql = r"insert into urls(href,title) value(" + "'" + tag.attrs['href'] + "'" + ',' + "'" + \
                          tag.attrs[
                              'title'] + "'" + ")"
                    print("编辑精选sql: ", sql)
                    self.cur.execute(sql)
                    self.coon.commit()

    def Hot_articles(self):  # 热点文章
        p_soup_list = self.soup.select(".aside >p")
        for p_soup in p_soup_list:
            if p_soup.get_text() == "热点文章":
                a_soup = p_soup.find_next("ul").select('li >.txt-box > .p1 >a')
                for tag in a_soup:
                    sql = r"insert into urls(href,title) value(" + "'" + tag.attrs['href'] + "'" + ',' + "'" + \
                          tag.attrs[
                              'title'] + "'" + ")"
                    print("热点文章sql: ", sql)
                    self.cur.execute(sql)
                    self.coon.commit()

    def Custom_hotspot_source_Text(self, text_list):  # 自定义热点文本
        a = "https://weixin.sogou.com/weixin?type=2&s_from=input&query="
        for text in text_list:
            response = requests.get(a + text, headers=headers, proxies=self.proxies)
            print(response.text)

    def Custom_hotspot_source_Url(self, url_list):  # 热点来源---链接
        pass

    def Hot_event_sources_of_other_websites(self, list):  # 选定某个网站作为外来热点来源-----写个爬虫去定向的爬取该网站的热点作为文本输入
        pass

    def input_text(self, text_list):  # 搜文章
        a = "https://weixin.sogou.com/weixin?type=2&s_from=input&query="
        for text in text_list:
            response = requests.get(a + text, headers=headers, proxies=self.proxies)
            print(response.text)

    def Crawling_article(self, text_list):  # 搜公众号
        a = "https://weixin.sogou.com/weixin?type=1&s_from=input&query="
        for text in text_list:
            response = requests.get(a + text, headers=headers, proxies=self.proxies)
            print(response.text)

    def Hot(self, num=20, pd=0):  # 分类--热门--提取相关文章链接  flag=False, 是否加载更多，默认加载20条，num=20，自定义加载多少条
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    # -----------------------------  开始 pc()函数为分类爬取中所需的常用函数，所以单独提出来。--------------------------------------
    def pc(self, pn, pd):
        if pn >= 1:
            url = "https://weixin.sogou.com/pcindex/pc/pc_" + str(pd) + "/" + str(pn) + ".html"

        else:

            url = "https://weixin.sogou.com/pcindex/pc/pc_" + str(pd) + "/pc_" + str(pd) + ".html"
        print("url:", url)
        a = "li > .txt-box > h3 > a "
        res = requests.get(url, headers=headers, proxies=self.proxies).content.decode("utf8")
        self.soup = BeautifulSoup(res, 'lxml')
        a_soup = self.soup.select(a)
        print(a_soup)
        for tag in a_soup:
            sql = r"insert into urls(href,title) value(" + "'" + tag.attrs['href'] + "'" + ',' + "'" + \
                  tag.text + "'" + ")"
            print("分类--热门sql: ", sql)
            self.cur.execute(sql)
            self.coon.commit()

    # ----------------------------  结束  pc() ----------------------------------------------------------------------------

    def Funny(self, num=20, pd=1):
        print("Funny")
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)
            print("可以")

    def Honyaradoh(self, num=20, pd=2):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn, pd):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Private_talk(self, num=20, pd=3):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Eight_trigrams(self, num=20, pd=4):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Technocrats(self, num=20, pd=5):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Financial_fans(self, num=20, pd=6):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Car_control(self, num=20, pd=7):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Life_home(self, num=20, pd=8):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Fashion_circle(self, num=20, pd=9):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Parenting(self, num=20, pd=10):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Travel(self, num=20, pd=11):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Workplace(self, num=20, pd=12):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def delicious_food(self, num=20, pd=13):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def history(self, num=20, pd=14):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def education(self, num=20, pd=15):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def constellation(self, num=20, pd=16):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Sports(self, num=20, pd=17):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def military(self, num=20, pd=18):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def game(self, num=20, pd=19):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def cute_pet(self, num=20, pd=20):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pn, pd)

    def Home_page_hot(self, num=20, pd=21):
        pn = 0
        if num > 20:
            pn = num / 20
            for n in range(pn):
                self.pc(n, pd)
            print("再一次执行这个函数")
            return "函数已执行完！"
        else:
            self.pc(pd)

