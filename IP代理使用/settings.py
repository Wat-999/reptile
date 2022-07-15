'''
*****配置文件*****
作用：便于用户设置输入，程序运行时从此文件读取参数属性，以便程序  明确执行  “动作”
'''

set_dir = {
    #   热点事件爬取（为以下三类）
    #            微信公众号热点来源（子集有三类）
    # 搜索热词
    'Search_hot_words': True,
    # 编辑精选
    'Editor_s_selection': True,
    # 热点文章
    'Hot_articles': True,

    #            自定义热点来源
    # 文本的形式--列表
    'Custom_hotspot_source_Text': True,
    # 若 Custom_hotspot_source_List:True 请在此处列表添加热点来源---文本
    'text_list': [],
    # 链接的形式--列表
    'Custom_hotspot_source_Url': True,
    # 若 Custom_hotspot_source_Url:True 请在此处列表添加热点来源---链接
    'Custom_hotspot_source_Url_List': '[]',

    #            其他网站的热点事件来源
    # 提取文本--列表
    'Hot_event_sources_of_other_websites': False,
    # 若 Hot_event_sources_of_other_websites:True 请在此处列表添加热点事件来源---文本
    'Hot_event_sources_of_other_websites_List': [],
    #            输入关键字文本爬取
    # 在此处输入文本
    'text': [],
    'input_text': False,
    # 爬取文章
    'Crawling_article': False,
    # 爬取公众号
    'Crawling_official_account': False,
    #            微信公众号分类爬取--加载到更多
    # 热门
    'Hot': True,
    # 搞笑
    'Funny': True,
    # 养生堂
    'Honyaradoh': False,
    # 私房话
    'Private_talk': False,
    # 八卦精
    'Eight_trigrams': False,
    # 科技咖
    'Technocrats': False,
    # 财经迷
    'Financial_fans': False,
    # 汽车控
    'Car_control': False,
    # 生活家
    'Life_home': False,
    # 时尚圈
    'Fashion_circle': False,
    # 育儿
    'Parenting': False,
    # 旅游
    'Travel': False,
    # 职场
    'Workplace': False,
    # 美食
    'delicious_food': False,
    # 历史
    'history': False,
    # 教育
    'education': False,
    # 星座
    'constellation': False,
    # 体育
    'Sports': False,
    # 军事
    'military': False,
    # 游戏
    'game': False,
    # 萌宠
    'cute_pet': False,
    # 主页热推
    'Home_page_hot': False,

}


class configure():
    def __init__(self):
        self.Search_hot_words = set_dir.get('Search_hot_words')
        self.Editor_s_selection = set_dir.get('Editor_s_selection')
        self.Hot_articles = set_dir.get('Hot_articles')
        self.Custom_hotspot_source_Text = set_dir.get('Custom_hotspot_source_Text')
        self.text_list = set_dir.get('text_list')
        self.Custom_hotspot_source_Url = set_dir.get('Custom_hotspot_source_Url')
        self.Custom_hotspot_source_Url_List = set_dir.get('Custom_hotspot_source_Url_List')
        self.Hot_event_sources_of_other_websites = set_dir.get('Hot_event_sources_of_other_websites')
        self.input_text = set_dir.get('input_text')
        self.Crawling_article = set_dir.get('Crawling_article')
        self.Crawling_official_account = set_dir.get('Crawling_official_account')
        self.Hot = set_dir.get('Hot')
        self.Funny = set_dir.get('Funny')
        self.Honyaradoh = set_dir.get('Honyaradoh')
        self.Private_talk = set_dir.get('Private_talk')
        self.Eight_trigrams = set_dir.get('Eight_trigrams')
        self.Technocrats = set_dir.get('Technocrats')
        self.Financial_fans = set_dir.get('Financial_fans')
        self.Car_control = set_dir.get('Car_control')
        self.Life_home = set_dir.get('Life_home')
        self.Fashion_circle = set_dir.get('Fashion_circle')
        self.Parenting = set_dir.get('Parenting')
        self.Travel = set_dir.get('Travel')
        self.Workplace = set_dir.get('Workplace')
        self.delicious_food = set_dir.get('delicious_food')
        self.history = set_dir.get('history')
        self.education = set_dir.get('education')
        self.constellation = set_dir.get('constellation')
        self.Sports = set_dir.get('Sports')
        self.military = set_dir.get('military')
        self.game = set_dir.get('game')
        self.cute_pet = set_dir.get('cute_pet')
        self.Home_page_hot = set_dir.get('Home_page_hot')


