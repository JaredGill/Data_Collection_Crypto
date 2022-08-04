from lib2to3.pgen2 import driver
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import uuid
import numpy as np
import time
import urllib.request
import os
import json

class Scraper:

    def __init__ (self, URL: str = "https://coinmarketcap.com/"):
        self.driver = webdriver.Edge()
        #URL = "https://coinmarketcap.com/"
        self.driver.get(URL)
        self.link_list = []
        self.url_list = []
        self.img_list = []
        self.img_name_list = []
        self.delay = 10
        # self.dict = {'CryptoName': [], 'UUID': [], 'URL': [], 'CurrentPrice': [], '24hrLowPrice': [], '24HighPrice': [], 'MarketCap': [], 'FullyDilutedMarketCap': [],
        #                 'Volume': [], 'Volume/MarketCap': [], 'CirculatingSupply': [], 'Image': []}
        self.dict_list = []

    #"_accept_method" = private method
    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cmc-cookie-policy-banner"]')))
            self.accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@class="cmc-cookie-policy-banner__close"]')
            self.accept_cookies_button.click()
            time.sleep(1)
            #return true for test
        except TimeoutException:
            print("Cookies are automatically accepted when browsing coinmarket.")
            #return flase for test

    #method to select GBP for currency
    def change_currency(self):
        try:
            settings_button = self.driver.find_element(by=By.XPATH, value='//*[@class="sc-1pyr0bh-0 bSnrp sc-1g16avq-0 kBKzKs"]')
            settings_button.click()
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="vxp8h8-0 VMCHA"]')))
            select_currency_button = self.driver.find_element(by=By.XPATH, value='//button[@data-qa-id="button-global-currency-picker"]')
            select_currency_button.click()
            currency = self.driver.find_element(by=By.XPATH, value='//*[@class="ig8pxp-0 jaunlC"]')
            time.sleep(2)
            currency.click()
        except:
            pass

    #public
    def get_links(self):
        self.coin_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="h7vnx2-1 bFzXgL"]//div[@class="sc-16r8icm-0 escjiH"]')
        #coin_list = coin_container.find_elements(by=By.XPATH, value='.//div[@class="sc-16r8icm-0 escjiH"]')
        for crypto_coin in self.coin_container:
            a_tag = crypto_coin.find_element(by=By.TAG_NAME, value='a')
            self.link = a_tag.get_attribute('href')
            self.link_list.append(self.link)
        
        for x in self.link_list:
            if x not in self.url_list:
                self.url_list.append(x)
        #to get unique links np.unique was tested, but it sorted links in alphabetical order
        #which is not wanted as the list should be top 100 popular cryptos
        #print(np.unique(self.link_list))

    #public
    def data_scrape(self):
        i = 0
        j = 0
        self.link_counter = 0
        while i < 3:
        #while i < len(self.url_list):
            URL = self.url_list[j]
            self.driver.get(URL)
            self.get_image()
            self.get_text_data()
            self.dict_list.append(self.dict_data)
            self.local_save()
            j += 1
            i += 1
            self.link_counter += 1
        #self.dict_list.append(self.nested_dict)
        #return dict_list
        
    #public
    def get_image(self):
        image_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="sc-16r8icm-0 gpRPnR nameHeader"]')
        for image in image_container:
            #containers are used as directly searching for elements can through error is they are altered on website
            img_tag = image.find_element(by=By.TAG_NAME, value='img')
            self.img = img_tag.get_attribute('src')
            self.img_list.append(self.img)
            # self.img_name = img_tag.get_attribute('alt')
            # self.img_name_list.append(self.img_name)
            #return image src -> is it the same for test (test_src)
            time.sleep(3)
            
    #public
    def get_text_data(self):
        # #dict for xpaths
        # #make dict with value
        # new_dict = {}
        # for key, value in self.nested_dict.items():
        #     #iterates through the keys and values ->
        #     try:
        #         if key == "etc":
        #             try: 
        #                 test = self.driver.find_elements(by=By.XPATH)
        #             except:
        #                 pass
        #         web_element = self.driver.find_elements(by=By.XPATH)

        # #extract element by xpath to test -> find.element not find.elements
        
        # for key, xpath
        price_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="sc-16r8icm-0 kjciSH priceSection"]')
        for price in price_container:
            price_tag = price.find_element(by=By.XPATH, value='//div[@class="priceValue "]').text
            low_tag = price.find_element(by=By.XPATH, value='//div[@class="sc-16r8icm-0 lipEFG"]//span[@class="n78udj-5 dBJPYV"]').text
            high_tag = price.find_element(by=By.XPATH, value='//div[@class="sc-16r8icm-0 SjVBR"]//span[@class="n78udj-5 dBJPYV"]').text
            

        title = self.driver.find_element(by=By.XPATH, value='//h2[@class="sc-1q9q90x-0 jCInrl h1"]').text
        self.id = title.replace('\n', ' (') + ")"

        
        values_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="statsValue"]')
        
        my_uuid = uuid.uuid4().hex
        #self.uuid_list.append(self.my_uuid)

        self.dict_data = {'CryptoName': self.id, 'UUID': my_uuid, 'URL': self.link_list[self.link_counter], 'CurrentPrice': price_tag, 
                            '24hrLowPrice': low_tag, '24hrHighPrice': high_tag, 'MarketCap': values_container[0].text, 
                            'FullyDilutedMarketCap': values_container[1].text, 'Volume': values_container[2].text, 'Volume/MarketCap': values_container[3].text, 
                            'CirculatingSupply': values_container[4].text, 'Image': self.img}
        

    #1 large json for text data
    #1 image data table
    #1 image folder containing downloaded 
    #read large json into pandas dataframe
    #strip the £ from all prices wtih pandas
        #read in json
        #in jypter notebook make the transformations
    #seperate dataframe from images

    def local_save(self):
        
        path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/{self.id}"
        if not os.path.exists(path):
            os.makedirs(path)
        
        if not os.path.exists(f"./raw_data/{self.id}/data.json"):
            with open(f"./raw_data/{self.id}/data.json", "w") as data:
                json.dump(self.dict_data, data)

        image_folder_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/{self.id}/images"
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)
        
        image_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/{self.id}/images/{self.id}_logo.jpeg"
        urllib.request.urlretrieve(self.img, image_path)
        
            

    def search_bar(self):
        self.search_bar = driver.find_element(by=By.XPATH, value='//*[@class="zafg3t-1 gaWePq"]')
        self.search_bar.click()
        self.search_bar.send_keys("method")
        self.search_bar.send_keys(Keys.RETURN)

    def scroll_bottom(self):
        #scroll, grab links then continue to next 20 elements
        max_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        scroll_down_y_axis = 2000

        while scroll_down_y_axis < max_page_height:
            self.driver.execute_script(f"window.scrollTo(0, {scroll_down_y_axis});")
            time.sleep(5)
            Scraper.get_links(self)
            scroll_down_y_axis += 2500

def scraper():
    scraper = Scraper()
    time.sleep(3)
    scraper.accept_cookies()
    scraper.change_currency()
    scraper.scroll_bottom()
    #print(scraper.url_list)
    # print(len(scraper.url_list))
    scraper.data_scrape()
    # print(scraper.img_list)
    # print(len(scraper.img_list))
    # #print(scraper.img_name_list)
    # print(scraper.price_list)
    # print(scraper.low_list)
    # print(scraper.high_list)
    # print(scraper.unq_id)
    # print(scraper.uuid_list)
    # print(scraper.market_cap_list)
    # print(scraper.fd_market_cap_list)
    # print(scraper.volume_list)
    # print(scraper.vol_mc_list)
    # print(scraper.circ_supply_list)
    #print(scraper.uuid_list)
    #print(scraper.dict)
    #print(scraper.nested_dict)
    print(scraper.dict_list)

    exit()


if __name__ == '__main__':
    scraper()


