from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException , TimeoutException , WebDriverException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import multiprocessing as mp
import pandas as pd
import numpy as np
import time
import datetime
import sys


class agoda_crawl(object):
    def __init__(self , city , start_date , end_date , room_num , adults_num , children_num , cpu_core , pos_x = 0 , pos_y = 0 , size_x = 500 , size_y = 500):
        self.city = city
        self.adults_num = adults_num
        self.room_num = room_num
        self.children_num = children_num
        self.start_date = datetime.date(start_date[0] , start_date[1] , start_date[2])
        self.end_date = datetime.date(end_date[0] , end_date[1] , end_date[2])
        self.cpu_core = cpu_core
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def num_confirm(self):
        if self.room_num < 1: sys.exit('Please reselect number of room!!')
        if self.adults_num < 1: sys.exit('Please reselect number of adult!!')
        if self.adults_num < self.room_num: sys.exit('Please reselect number of room & adult!!')

    def date_confirm(self):
        if (self.start_date - datetime.date.today()).days < 0:
            sys.exit('Please reselect departrue date!!')
                    
    def get_web(self , driver):
        self.driver = driver
        self.driver.set_window_position(self.pos_x , self.pos_y)
        self.driver.set_window_size(self.size_x , self.size_y)
        self.driver.get("https://www.agoda.com/zh-tw/")
        time.sleep(5)    
 
    # 按掉彈出式廣告
    def delete_pop_ad(self):
        try:
            self.driver.find_element_by_class_name('ab-close-button').click()
        except NoSuchElementException:
            pass 
    
    def select_city(self):
        print('cpu_core : {} , step1.輸入城市、區域、景點或住宿名稱 → 開始'.format(self.cpu_core))
        try:
            self.delete_pop_ad()
            self.driver.find_element_by_xpath("//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").click()
            self.driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").clear()
            self.driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(u"{}".format(self.city))
            self.driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(Keys.ENTER)
            time.sleep(2)
            self.driver.find_element_by_xpath("//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/ul[1]/li[1]/ul[1]/li[1]").click()
        except WebDriverException:
            print('cpu_core : {} fuck you!!!'.format(self.cpu_core))
            self.delete_pop_ad()
            time.sleep(2)
            self.driver.find_element_by_xpath("//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").click()
            self.driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").clear()
            self.driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(u"{}".format(self.city))
            self.driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(Keys.ENTER)
            time.sleep(2)
            self.driver.find_element_by_xpath("//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/ul[1]/li[1]/ul[1]/li[1]").click()
        print('cpu_core : {} , step1.輸入城市、區域、景點或住宿名稱 → 結束'.format(self.cpu_core))
        
    def month_delta(self):
        soup = BeautifulSoup(self.driver.page_source , 'html5lib')
        current_year_month = soup.select("[class='DayPicker-Caption']")
        current_year = int(current_year_month[0].text[0:5].rstrip('年'))
        current_month = int(current_year_month[0].text[5:].rstrip('月'))
        count = 0
        while True:
            current_month = current_month + 1
            if current_month == 13:
                current_month = 1
                current_year = current_year + 1
            count = count + 1    
            if current_year == self.start_date.year and current_month == self.start_date.month:
                break   
        self.month_moving = count    
    
    def select_date(self):
        print('cpu_core : {} , step2.選擇日期 → 開始'.format(self.cpu_core))
        self.delete_pop_ad()
        for _ in range(0 , self.month_moving):
            self.driver.find_element_by_xpath("//span[contains(@class,'ficon ficon-18 ficon-edge-arrow-right')]").click()
        self.driver.find_element_by_xpath("//div[@class='DayPicker-wrapper']//div[1]//div[3]//div[1]//div[7]").click()
        self.driver.find_element_by_xpath("//div[@class='DayPicker-wrapper']//div[1]//div[3]//div[3]//div[7]").click()
        print('cpu_core : {} , step2.選擇日期 → 結束'.format(self.cpu_core))
        time.sleep(5)
        
    def select_room_type(self):
        print('cpu_core : {} , step3.選擇旅遊形式 → 開始'.format(self.cpu_core))
        self.delete_pop_ad()
        # 選擇家庭旅遊
        self.driver.find_element_by_xpath("//div[@class='Popup__container Popup__container--garage-door']//div[3]//div[1]").click()
        print('cpu_core : {} , step3.選擇旅遊形式 → 結束'.format(self.cpu_core))
        time.sleep(2)

        print('cpu_core : {} , step4.選擇成人人數 → 開始'.format(self.cpu_core))
        self.delete_pop_ad()
        # 決定決定幾位大人(預設是2位大人)
        for people in range(0 , self.adults_num - 2):
            time.sleep(2)
            self.driver.find_element_by_xpath("//div[@class='SegmentOccupancy__occupancy']//div[2]//span[4]//*[local-name()='svg']").click()
        print('cpu_core : {} , step4.選擇成人人數 → 結束'.format(self.cpu_core))
        time.sleep(2)

        print('cpu_core : {} , step5.選擇客房房數 → 開始'.format(self.cpu_core))
        self.delete_pop_ad()
        # 決定幾間客房(預設是1間客房)
        for room in range(0 , self.room_num - 1):
            time.sleep(2)
            self.driver.find_element_by_xpath("//div[@class='OccupancySelector OccupancySelector--travelWithKids']//div[1]//span[4]//*[local-name()='svg']").click()
        print('cpu_core : {} , step5.選擇客房房數 → 結束'.format(self.cpu_core))
        time.sleep(2)
        
        print('cpu_core : {} , step6.選擇兒童人數 → 開始'.format(self.cpu_core))
        self.delete_pop_ad()
        # 幾位兒童(預設是0位兒童)
        for children in range(0 , self.children_num - 0):
            time.sleep(2)
            self.driver.find_element_by_xpath("//div[3]//span[4]//*[local-name()='svg']").click()
        print('cpu_core : {} , step6.選擇兒童人數 → 結束'.format(self.cpu_core))    
        time.sleep(2)

    def press_search_button(self):
        print('cpu_core : {} , step7.開始查詢 → 開始'.format(self.cpu_core))
        self.delete_pop_ad()
        self.driver.find_element_by_xpath("//div[@id='SearchBoxContainer']/div/div/div/div/div/div[4]/div/div/div/div[3]/i").click()
        self.driver.find_element_by_xpath("//div[@id='SearchBoxContainer']/div[2]/button/div").click()
        print('cpu_core : {} , step7.開始查詢 → 結束'.format(self.cpu_core))
        time.sleep(5)
        # 若有選擇兒童，會在按下search button後的頁面出現一個小視窗(系統預設兒童年齡8歲)，需要按掉才能繼續後續的步驟
        try:
            self.driver.find_element_by_xpath("//div[@id='SearchBoxContainer']/div/div/div[4]/div/div/div/div[2]").click()
        except NoSuchElementException:
            pass

    def start_crawl(self):
        self.data_pd = pd.DataFrame(columns = ['旅店名稱' , '鄰近地區' , '旅客評分' , '旅客評鑑數目' , '旅店當天價格'])
        while True:
            time.sleep(5 + np.random.randint(0 , 5))
            soup = BeautifulSoup(self.driver.page_source , 'html5lib')
        
            current_page = soup.select("[data-selenium='pagination-text']")[0].text.split('/')[0]
            total_page = soup.select("[data-selenium='pagination-text']")[0].text.split('/')[1]
            current_page = int(current_page.replace('第' , '').replace('頁' , ''))
            total_page = int(total_page.replace(' 共' , '').replace('頁' , ''))
            print('\ncpu_core : {} , current page : {} , total page : {}'.format(self.cpu_core , current_page , total_page))

            # 必須將網頁慢慢往下滾動，才能獲得全部旅店的資訊
            # 網頁往下滾動時，y_location會慢慢變大，當停止變大時，代表網頁已經滾動到最下面
            # 接下來即可使用BeautifulSoup獲取網頁內容
            y_location_set = []
            count_rolldown = 0
            y_current = 0
            while True:
                # 若跳出其他網頁，則將目前頁面轉回目標頁面
                handles = self.driver.window_handles
                if len(handles) == 2:
                    self.driver.switch_to_window(handles[1])
                    self.driver.close()
                    self.driver.switch_to_window(handles[0])
                        
                y_location = self.driver.find_element_by_xpath("//span[@id='paginationPageCount']").location['y']
                print('cpu_core : {} , page : {} , y_location : {} , count : {}'.format(self.cpu_core , current_page , y_location , count_rolldown))
                y_location_set.append(y_location)
                y_location_set = np.array(y_location_set)
                if y_location_set[-1] != y_current:
                    y_current = y_location_set[-1]
                    count_rolldown = 0
                elif y_location_set[-1] == y_current:
                    count_rolldown += 1
        
                if count_rolldown > 200:
                    y_location_set = []
                    count_rolldown = 0
                    y_current = 0
                    break
                y_location_set = list(y_location_set)
        
                # 每次往下滾動200
                self.driver.execute_script("window.scrollBy(0,100)")

            # 使用BeautifulSoup獲取網頁內容
            time.sleep(10)
            soup = BeautifulSoup(self.driver.page_source , 'html5lib')
            temp_name , temp_loc , temp_rate , temp_evaluation_num , temp_price = [] , [] , [] , [] , []
            for step , all_part in enumerate(soup.select("[class='JacketContent JacketContent--Empty']")):
        
                # 獲取旅店名稱
                if len(all_part.select("[data-selenium='hotel-name']")) != 0:
                    temp_name.append(all_part.select("[data-selenium='hotel-name']")[0].text)
                else:
                    temp_name.append('no info')
        
                # 獲取鄰近地區
                if len(all_part.select("[data-selenium='area-city-text']")) != 0:
                    temp_loc.append(all_part.select("[data-selenium='area-city-text']")[0].text.rstrip(' - 查看地圖'))
                else:
                    temp_loc.append('no info')
        
                # 獲取旅客評分
                if len(all_part.select("[class='sc-AxheI elHqDQ']")) != 0:
                    temp_rate.append(all_part.select("[class='sc-AxheI elHqDQ']")[0].text)
                else :
                    temp_rate.append('no info')
        
                # 獲取旅客評鑑數目
                if len(all_part.select("[class='sc-AxheI rbZVq sc-AxirZ fBDjam']")) != 0:
                    temp_evaluation_num.append(all_part.select("[class='sc-AxheI rbZVq sc-AxirZ fBDjam']")[0].text.split(' ')[0])
                else: temp_evaluation_num.append('no info')

                # 獲取旅店當天價格
                if len(all_part.select("[class='PropertyCardPrice__Value']")) != 0:
                    temp_price.append(all_part.select("[class='PropertyCardPrice__Value']")[0].text)
                elif len(all_part.select("[data-element-name='final-price']")) != 0:
                    temp_price.append(all_part.select("[data-element-name='final-price']")[0].text.split(' ')[-1])
                else: temp_price.append('no info')
            
            data_pd_temp = pd.concat([pd.DataFrame(temp_name) , 
                                      pd.DataFrame(temp_loc) ,
                                      pd.DataFrame(temp_rate) ,
                                      pd.DataFrame(temp_evaluation_num) ,
                                      pd.DataFrame(temp_price)] , axis = 1)
            if len(data_pd_temp) != 0:
                data_pd_temp.columns = ['旅店名稱' , '鄰近地區' , '旅客評分' , '旅客評鑑數目' , '旅店當天價格']
                self.data_pd = pd.concat([self.data_pd , data_pd_temp] , axis = 0)


            # 當找不到"paginationNext"這個元素，代表很可能已經到了最後一頁，即可停止爬蟲
            try:
                self.driver.find_element_by_id("paginationNext").click()
                print('\ncpu_core : {} , NOT YET!!!'.format(self.cpu_core))
            except NoSuchElementException:
                try:
                    # 在5秒內看"paginationNext"這個元素有沒有出現，如果沒有出現，代表已經到了最後一頁，即可停止爬蟲
                    wait = ui.WebDriverWait(self.driver , 5)
                    wait.until(lambda driver: self.driver.find_element_by_id("paginationNext"))
                except TimeoutException:
                    print('\ncpu_core : {} , FINSH CRAWLING!!!'.format(self.cpu_core))
                    break


def crawl_fun(agoda_crawler , city_name , q):
    agoda_crawler.num_confirm()
    agoda_crawler.date_confirm()

    driver = webdriver.Chrome()
    agoda_crawler.get_web(driver)

    agoda_crawler.select_city()
    agoda_crawler.month_delta()
    agoda_crawler.select_date()
    agoda_crawler.select_room_type()
    agoda_crawler.press_search_button()
    agoda_crawler.start_crawl()

    q.put([city_name , agoda_crawler.data_pd])


if __name__ == '__main__':

    Taipei = agoda_crawl(city = '台北' ,                    # city
                         start_date = [2021 , 4 , 10] ,     # start_date
                         end_date = [2021 , 4 , 17] ,       # end_date
                         room_num = 3 ,                     # room_num
                         adults_num = 4 ,                   # adults_num
                         children_num = 2 ,                 # children_num
                         cpu_core = 1 ,                     # cpu_core
                         pos_x = 0 ,
                         pos_y = 0 ,
                         size_x = 1000 ,
                         size_y = 900)

    Taichung = agoda_crawl(city = '台中' ,                  # city
                           start_date = [2021 , 4 , 10] ,   # start_date
                           end_date = [2021 , 4 , 17] ,     # end_date
                           room_num = 3 ,                   # room_num
                           adults_num = 4 ,                 # adults_num
                           children_num = 2 ,               # children_num
                           cpu_core = 2 ,                   # cpu_core
                           pos_x = 800 ,
                           pos_y = 0 ,
                           size_x = 1000 ,
                           size_y = 900)

    city_name_list = ['Taipei' , 'Taichung']
    crawl_list = [Taipei , Taichung]

    manager = mp.Manager()
    q = manager.Queue()
    processes = []
    for i in range(0 , 2):
        processes = []
        p = mp.Process(target = crawl_fun , args = [crawl_list[i] , city_name_list[i] , q])
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    for _ in range(0 , 2):
        [city_name , agoda_data] = q.get()
        agoda_data.to_csv('{}_agoda_data.csv'.format(city_name) , encoding = 'utf_8_sig')