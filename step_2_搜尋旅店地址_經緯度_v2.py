import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException , TimeoutException , WebDriverException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
import pyautogui

# raw_data = pd.read_csv('Taipei_crawl_result.csv' , index_col = 0)
# raw_data = pd.read_csv('Taipei_crawl_result.csv' , index_col = 0)
# raw_data.replace({'【初登場】尚無評價' : np.nan , 'no info' : np.nan} , inplace = True)

# raw_data['行政區'] = raw_data['鄰近地區'].apply(lambda x : x.split(',')[0])
# raw_data['行政區'] = raw_data['行政區'].replace({'台北車站' : '中正區' , '西門町' : '萬華區' , '九份' : '瑞芳區'})
# raw_data.drop(columns = ['鄰近地區'] , inplace = True)

# raw_data['旅客評分'] = raw_data['旅客評分'].str.replace(',' , '').astype(float)
# raw_data['旅客評鑑數目'] = raw_data['旅客評鑑數目'].str.replace(',' , '').astype(float)
# raw_data['旅店當天價格'] = raw_data['旅店當天價格'].str.replace(',' , '').astype(float)

raw_data = pd.read_csv('Taipei_crawl_result.csv' , index_col = 0)
driver = webdriver.Chrome()
driver.get('https://www.google.com.tw/maps')
driver.maximize_window()
js = "window.open('https://www.google.com.tw/maps')"
page_num = 4
for _ in range(0 , page_num - 1):
    driver.execute_script(js)
time.sleep(5)

hotel_subsets = []
temp = []
for hotel in list(raw_data['旅店名稱']):
    temp.append(hotel)
    if len(temp) == page_num:
        hotel_subsets.append(temp)
        temp = []
if len(temp) != page_num: hotel_subsets.append(temp)

hotel_lat_log = []
for index , hotel_subset in enumerate(hotel_subsets):
    if len(hotel_subset) != page_num:
        for _ in range(0 , page_num - len(hotel_subset)):
            driver.close()

    # 搜尋旅店位置
    handles = driver.window_handles
    for i , (handle , hotel_name) in enumerate(zip(handles , hotel_subset)):
        driver.switch_to_window(handle)
        driver.find_element_by_id("searchboxinput").click()
        driver.find_element_by_id("searchboxinput").clear()
        driver.find_element_by_id("searchboxinput").send_keys(u"{}".format(hotel_name))
        driver.find_element_by_id("searchboxinput").send_keys(Keys.ENTER)
    time.sleep(5)

    # 移動滑鼠並點擊右鍵
    for i , handle in enumerate(handles):
        driver.switch_to_window(handle)
        pyautogui.moveTo(1736 , 995 , duration = 0.5)
        pyautogui.rightClick()
    time.sleep(5)

    # 獲取經緯度
    for i , (handle , hotel_name) in enumerate(zip(handles , hotel_subset)):
        driver.switch_to_window(handle)
        soup = BeautifulSoup(driver.page_source , 'html5lib')
        position = soup.select("[class='action-menu-entry-text']")[0].text
        hotel_lat_log.append([hotel_name , float(position.split(',')[0]) , float(position.split(',')[1])])


hotel_lat_log = pd.DataFrame(hotel_lat_log)
hotel_lat_log.columns = ['旅店名稱' , 'lat' , 'log']
hotel_lat_log.set_index('旅店名稱' , inplace = True , drop = True)
hotel_lat_log = hotel_lat_log.reindex(raw_data['旅店名稱' ]) # 強迫hotel_lat_log的順序跟raw_data相同
raw_data.set_index('旅店名稱' , inplace = True , drop = True)
raw_data = pd.concat([raw_data , hotel_lat_log] , axis = 1)
raw_data['旅店名稱'] = raw_data.index
raw_data.to_csv('Taipei_crawl_result_經緯度_v2.csv')