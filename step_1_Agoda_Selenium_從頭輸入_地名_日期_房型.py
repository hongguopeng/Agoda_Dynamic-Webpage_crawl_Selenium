from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException , TimeoutException , WebDriverException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

# 按掉彈出式廣告
def delete_pop_ad():
    try:
        driver.find_element_by_class_name('ab-close-button').click()
    except NoSuchElementException:
        pass

# 若跳出其他網頁，則將目前頁面轉回目標頁面
def delete_webpage():
    handles = driver.window_handles
    if len(handles) == 2:
        driver.switch_to_window(handles[1])
        driver.close()
        driver.switch_to_window(handles[0])

driver = webdriver.Chrome()
driver.get("https://www.agoda.com/zh-tw/")
time.sleep(5)

print('1.輸入城市、區域、景點或住宿名稱 → 開始')
try:
    delete_pop_ad()
    driver.find_element_by_xpath("//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").click()
    driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").clear()
    driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(u"台北")
    driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element_by_xpath("//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/ul[1]/li[1]/ul[1]/li[1]").click()
except WebDriverException:
    print('fuck you!!!')
    delete_pop_ad()
    time.sleep(2)
    driver.find_element_by_xpath("//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").click()
    driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").clear()
    driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(u"台北")
    driver.find_element_by_xpath(u"//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]").send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element_by_xpath("//body/div[@id='home-react-root']/div[1]/section[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/ul[1]/li[1]/ul[1]/li[1]").click()
print('1.輸入城市、區域、景點或住宿名稱 → 結束\n')

print('2.選擇日期 → 開始')
delete_pop_ad()
for i in range(0 , 4): # 選擇日期的窗格滑動4次，ex:現在12月，若想選擇4月的房間，就滑動4次；而日期挑在4/10~4/17
    driver.find_element_by_xpath("//span[contains(@class,'ficon ficon-18 ficon-edge-arrow-right')]").click()
driver.find_element_by_xpath("//div[@class='DayPicker-wrapper']//div[1]//div[3]//div[3]//div[6]").click()
driver.find_element_by_xpath("//div[@class='DayPicker-wrapper']//div[1]//div[3]//div[4]//div[1]").click()
print('2.選擇日期 → 結束\n')
time.sleep(2)

print('3.選擇旅遊形式 → 開始')
delete_pop_ad()
# 選擇家庭旅遊
driver.find_element_by_xpath("//div[@class='Popup__container Popup__container--garage-door']//div[3]//div[1]").click()
print('3.選擇旅遊形式 → 結束\n')
time.sleep(2)

print('4.選擇成人人數 → 開始')
delete_pop_ad()
# 決定決定幾位大人(預設是2位大人)
for people in range(0 , 2 - 2):
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='SegmentOccupancy__occupancy']//div[2]//span[4]//*[local-name()='svg']").click()
print('4.選擇成人人數 → 結束\n')
time.sleep(2)

print('5.選擇客房房數 → 開始')
delete_pop_ad()
# 決定幾間客房(預設是1間客房)
for room in range(0 , 1 - 1):
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='OccupancySelector OccupancySelector--travelWithKids']//div[1]//span[4]//*[local-name()='svg']").click()
print('5.選擇客房房數 → 結束\n')
time.sleep(2)

print('6.選擇兒童人數 → 開始')
delete_pop_ad()
# 幾位兒童(預設是0位兒童)
for children in range(0 , 0 - 0):
    time.sleep(2)
    driver.find_element_by_xpath("//div[3]//span[4]//*[local-name()='svg']").click()
print('6.選擇兒童人數 → 結束\n')
time.sleep(2)

print('7.開始查詢 → 開始')
delete_pop_ad()
driver.find_element_by_xpath("//div[@id='SearchBoxContainer']/div/div/div/div/div/div[4]/div/div/div/div[3]/i").click()
driver.find_element_by_xpath("//div[@id='SearchBoxContainer']/div[2]/button/div").click()
print('7.開始查詢 → 結束\n')
time.sleep(5)
# 若有選擇兒童，會在按下search button後的頁面出現一個小視窗(系統預設兒童年齡8歲)，需要按掉才能繼續後續的步驟
try:
    if driver.find_element_by_xpath("//div[@class='OccupancySelector']").is_displayed():
        driver.find_element_by_xpath("//div[@id='SearchBoxContainer']/div/div/div[4]/div/div/div/div[2]").click()
except NoSuchElementException:
    pass

#-----------------------crawl_part-----------------------#
data_pd = pd.DataFrame(columns = ['旅店名稱' , '鄰近地區' , '旅客評分' , '旅客評鑑數目' , '旅店當天價格'])

while True:
    time.sleep(5 + np.random.randint(0 , 5))
    soup = BeautifulSoup(driver.page_source , 'html5lib')

    current_page = soup.select("[data-selenium='pagination-text']")[0].text.split('/')[0]
    total_page = soup.select("[data-selenium='pagination-text']")[0].text.split('/')[1]
    current_page = int(current_page.replace('第' , '').replace('頁' , ''))
    total_page = int(total_page.replace(' 共' , '').replace('頁' , ''))
    print('\ncurrent page : {} , total page : {}'.format(current_page , total_page))

    # 必須將網頁慢慢往下滾動，才能獲得全部旅店的資訊
    # 網頁往下滾動時，y_location會慢慢變大，當停止變大時，代表網頁已經滾動到最下面
    # 接下來即可使用BeautifulSoup獲取網頁內容
    y_location_set = []
    count_rolldown = 0
    y_current = 0
    while True:
        delete_webpage()

        y_location = driver.find_element_by_xpath("//span[@id='paginationPageCount']").location['y']
        print('page : {} , y_location : {} , count : {}'.format(current_page , y_location , count_rolldown))
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

        # 每次將網頁往下滾動200
        driver.execute_script("window.scrollBy(0,100)")

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") # 讓網頁頁面滾動到最底部

    # 使用BeautifulSoup獲取網頁內容
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source , 'html5lib')
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
        data_pd = pd.concat([data_pd , data_pd_temp] , axis = 0)

    # 當找不到"paginationNext"這個元素，代表很可能已經到了最後一頁，即可停止爬蟲
    try:
        driver.find_element_by_id("paginationNext").click()
        print('\nNOT YET!!!')
    except NoSuchElementException:
        try:
            # 在5秒內看"paginationNext"這個元素有沒有出現，如果沒有出現，代表已經到了最後一頁，即可停止爬蟲
            wait = ui.WebDriverWait(driver , 5)
            wait.until(lambda driver: driver.find_element_by_id("paginationNext"))
        except TimeoutException:
            print('\nFINSH CRAWLING!!!')
            break
        
data_pd.reset_index(inplace = True , drop = True)    
data_pd.to_csv('Taipei_crawl_result.csv')
#-----------------------crawl_part-----------------------#


#-----------------------demo-----------------------#
#driver.execute_script("window.scrollBy(0,50)") # 模擬網頁往下滾動，每次滾動距離50
#driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") # 讓網頁頁面滾動到最底部
#driver.execute_script("window.scrollTo(0,0)") # 讓網頁頁面滾動到最上方     
#-----------------------demo-----------------------#