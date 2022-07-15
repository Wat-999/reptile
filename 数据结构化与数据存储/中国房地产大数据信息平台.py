from selenium import webdriver

url = 'https://creis.fang.com/'
browser = webdriver.Chrome()

browser.get(url)
browser.switch_to.window(browser.window_handles[1])
data = browser.page_source

import re
p_name = '<td align="left" title="(.*?)">'

name = re.findall(p_name, data)
print(name)
import pandas as pd
tables = pd.read_html(data)
print(tables[0])




