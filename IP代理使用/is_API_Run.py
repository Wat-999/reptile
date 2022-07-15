'''
获取配置文件settings的输入给与相应的函数输出
'''

from API_Function import Functions
from settings import configure


class read_settings_run_func():
    def __init__(self, page, proxies):
        self.proxies = proxies
        self.page = page
        self.set = configure()
        self.func = Functions(self.page, self.proxies)
        self.test_settings()

    def test_settings(self):
        if self.set.Search_hot_words == True:
            self.func.Search_hot_words()
        else:
            print("mei")
        if self.set.Editor_s_selection == True:
            self.func.Editor_s_selection()
        else:
            print("mei")

        if self.set.Hot_articles == True:
            self.func.Hot_articles()
        else:
            print("mei")

        if self.set.Custom_hotspot_source_Text == True:
            self.func.Custom_hotspot_source_Text(self.set.text_list)
        else:
            print("mei")

        if self.set.Custom_hotspot_source_Url == True:
            self.func.Custom_hotspot_source_Url(self.set.Custom_hotspot_source_Url_List)
        else:
            print("mei")

        if self.set.Hot_event_sources_of_other_websites == True:
            self.func.Hot_event_sources_of_other_websites(self.set.Hot_event_sources_of_other_websites_List)
        else:
            print("mei")

        if self.set.input_text == True:
            self.func.input_text(self.set.text)
        else:
            print("mei")

        if self.set.Crawling_article == True:
            self.func.Crawling_article(self.set.text)
        else:
            print("mei")

        if self.set.Crawling_official_account == True:
            self.func.Crawling_official_account()
        else:
            print("mei")

        if self.set.Hot == True:
            self.func.Hot()
        else:
            print("mei")

        if self.set.Funny == True:
            self.func.Funny()
        else:
            print("mei")

        if self.set.Honyaradoh == True:
            self.func.Honyaradoh()
        else:
            print("mei")

        if self.set.Private_talk == True:
            self.func.Private_talk()
        else:
            print("mei")

        if self.set.Eight_trigrams == True:
            self.func.Eight_trigrams()
        else:
            print("mei")

        if self.set.Technocrats == True:
            self.func.Technocrats()
        else:
            print("mei")

        if self.set.Financial_fans == True:
            self.func.Financial_fans()
        else:
            print("mei")

        if self.set.Car_control == True:
            self.func.Car_control()
        else:
            print("mei")

        if self.set.Life_home == True:
            self.func.Life_home()
        else:
            print("mei")

        if self.set.Fashion_circle == True:
            self.func.Fashion_circle()
        else:
            print("mei")

        if self.set.Parenting == True:
            self.func.Parenting()
        else:
            print("mei")

        if self.set.Travel == True:
            self.func.Travel()
        else:
            print("mei")

        if self.set.Workplace == True:
            self.func.Workplace()
        else:
            print("mei")

        if self.set.delicious_food == True:
            self.func.delicious_food()
        else:
            print("mei")

        if self.set.history == True:
            self.func.history()
        else:
            print("mei")

        if self.set.education == True:
            self.func.education()
        else:
            print("mei")

        if self.set.constellation == True:
            self.func.constellation()
        else:
            print("mei")

        if self.set.Sports == True:
            self.func.Sports()
        else:
            print("mei")

        if self.set.military == True:
            self.func.military()
        else:
            print("mei")

        if self.set.game == True:
            self.func.game()
        else:
            print("mei")

        if self.set.cute_pet == True:
            self.func.cute_pet()
        else:
            print("mei")

        if self.set.Home_page_hot == True:
            self.func.Home_page_hot()
        else:
            print("mei")

