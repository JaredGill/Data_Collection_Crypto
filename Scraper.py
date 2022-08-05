from ast import Str
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
import pandas as pd

class Scraper:
    '''
    A scraper class for the website coinmarketcap to obtain the data values for price, supply, etc. 
    Uses the package selenium to connect and interact with the website.
    
    Parameters:
    ----------
    URL: str
        the URL of the website to be scraped
    
    Attributes:
    ----------
    driver: module
        calls the webdriver module to open a microsoft edge window
    url_list: list
        A list of every unique url in the websites page, each corresponding to a crypto coin
    img_list: list
        A list of the image links(for this website the only image is the coin logo)
    img_name_list: list
        A list of the alt tags for the logo's in the img_list
    delay: int
        the amount of time the webdriver will be timeout for, occuring when necessary to wait for a element on the webpage to load
    dict: dict
        A dictionary of lists, each list containing the .text data in order of market rank starting with bitcoin

    Methods:
    -------
    accept_cookies()
        Closes cookies popup
    
    change_currency()
        Changes currency data is displayed in
    
    get_link()
        Finds the links for each crytpo coin in the page

    get_image()
        Finds the coin's logo in its page

    scroll_bottom()
        Scrolls to the bottom of the page

    search_bar()
        Makes the search bar interactable

    local_save()
        Saves raw data in local storage

    get_text_data()
        Locates and returns the text data on a coins unique page

    data_scrape()
        Goes through each coin's link and scrapes data

    '''
    def __init__ (self, URL: str = "https://coinmarketcap.com/"):
        self.driver = webdriver.Edge()
        self.driver.get(URL)
        self.url_list = []
        self.img_list = []
        self.img_name_list = []
        self.delay = 10
        self.coin_data_dict = {'CryptoName': [], 'UUID': [], 'URL': [], 'CurrentPrice': [], '24hrLowPrice': [], '24hrHighPrice': [], 'MarketCap': [], 'FullyDilutedMarketCap': [],
                         'Volume': [], 'Volume/MarketCap': [], 'CirculatingSupply': []}

    #"_accept_method" = private method
    def accept_cookies(self):
        '''
        Waits for the accept cookies element to appear then closes it.
        '''
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
    #maybe change to have 3 letter currency in parameters and pass it in
    def change_currency(self):
        '''
        Opens the Select Currency button and selects British pound(GBP) when element is present.
        '''
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
        '''
        Locates each unique coin in the main contianer on the homepage by "a" tag, and saves the href as a link.
        The link_list saves all hrefs that have loaded on page as website has dynamic pages.
        The url_list contains all unique hrefs from the link_list 
        '''
        link_list = []
        url_list = []
        self.coin_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="h7vnx2-1 bFzXgL"]//div[@class="sc-16r8icm-0 escjiH"]')
        for crypto_coin in self.coin_container:
            a_tag = crypto_coin.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        
        for url in link_list:
            if url not in url_list:
                url_list.append(url)
                
        return url_list

    #public
    #maybe pass in the url list as a parameter
    def data_scrape(self, coins_to_scrape = 0):
        '''
        Iterates through url_list by calling self.get_links() function for get_text_data() and get_image() to scrape.
        Appends the URL in use to the coin_data dictionary so the arrays are the same length.
        Calls get_text_data() in the while loop to add data for each coins url.

        Parameters:
        ----------
        coins_to_scrape: int
            Amount of crypto coins to be scraped
        '''
        url_counter = 0
        coin_link_list = self.get_links()
        
        while url_counter < coins_to_scrape:
            URL = coin_link_list[url_counter]
            self.driver.get(URL)
            self.get_image()
            self.get_text_data()
            self.coin_data_dict['URL'].append(coin_link_list[url_counter])
            #self.local_save()
            url_counter += 1
        

    #public
    def get_image(self):
        '''
        Locates the coin's image logo by container, then returns its src and alt for img link and name respectively
        '''
        image_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="sc-16r8icm-0 gpRPnR nameHeader"]')
        for image in image_container:
            #containers are used as directly searching for elements can through error is they are altered on website
            img_tag = image.find_element(by=By.TAG_NAME, value='img')
            self.img = img_tag.get_attribute('src')
            self.img_list.append(self.img)
            # self.img_name = img_tag.get_attribute('alt')
            # self.img_name_list.append(self.img_name)
            #return image src -> is it the same for test (test_src)
            time.sleep(2)
            
    #public
    def get_text_data(self):
        '''
        Scrapes the data from the coin's specific webpage and appending them to the coin_data dictionary.
        This method is called in each iteration of the data_scrape method to populate the dictionary
        with each coins data.
        Price, 24hr low and high are obtained from the same container using specific xpaths and .text
        ID is found directly calling the unique class xpath.
        MarketCap, FullyDilutedMarketCap, Volume, Volume/MarketCap, CirculatingSupply are found in the same 
        container and using .text at specific positions in the containers list.
        A UUID was also generated using the package.
        
        '''
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
            self.coin_data_dict['CurrentPrice'].append(price_tag)
            low_tag = price.find_element(by=By.XPATH, value='//div[@class="sc-16r8icm-0 lipEFG"]//span[@class="n78udj-5 dBJPYV"]').text
            self.coin_data_dict['24hrLowPrice'].append(low_tag)
            high_tag = price.find_element(by=By.XPATH, value='//div[@class="sc-16r8icm-0 SjVBR"]//span[@class="n78udj-5 dBJPYV"]').text
            self.coin_data_dict['24hrHighPrice'].append(high_tag)


        title = self.driver.find_element(by=By.XPATH, value='//h2[@class="sc-1q9q90x-0 jCInrl h1"]').text
        id_tag = title.replace('\n', ' (') + ")"
        self.coin_data_dict['CryptoName'].append(id_tag)
        
        values_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="statsValue"]')
        self.coin_data_dict['MarketCap'].append(values_container[0].text)
        self.coin_data_dict['FullyDilutedMarketCap'].append(values_container[1].text)
        self.coin_data_dict['Volume'].append(values_container[2].text)
        self.coin_data_dict['Volume/MarketCap'].append(values_container[3].text)
        self.coin_data_dict['CirculatingSupply'].append(values_container[4].text)


        my_uuid = uuid.uuid4().hex
        self.coin_data_dict['UUID'].append(my_uuid)
        #self.uuid_list.append(self.my_uuid)

        
        return id_tag
        
    #1 large json for text data
    #1 image data table
    #1 image folder containing downloaded 
    #read large json into pandas dataframe
    #strip the £ from all prices wtih pandas
        #read in json
        #in jypter notebook make the transformations
    #seperate dataframe from images

    def local_save(self):
        '''
        Makes a directory for each unique coin and saves their raw data dict as a .json file.
        Also makes an images directory in each coin directory and saves logo image .jpeg
        '''
        crypto_name = self.get_text_data()
        path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/{crypto_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        
        if not os.path.exists(f"./raw_data/{crypto_name}/data.json"):
            with open(f"./raw_data/{crypto_name}/data.json", "w") as data:
                json.dump(self.dict_data, data)

        image_folder_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/{crypto_name}/images"
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)
        
        image_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/{crypto_name}/images/{crypto_name}_logo.jpeg"
        urllib.request.urlretrieve(self.img, image_path)
        

    def search_bar(self, text_search: Str = " test "):
        '''
        Opens the search bar and inputs text via parameter then clicks.

        Parameters:
        text_search: str
            The desired text to be searched.
        '''
        time.sleep(5)
        self.search_bar = self.driver.find_element(by=By.XPATH, value='//*[@class="zafg3t-1 gaWePq"]')
        self.search_bar.click()
        time.sleep(2)
        self.search_bar.send_keys(text_search)
        self.search_bar.send_keys(Keys.RETURN)

    def scroll_bottom(self):
        '''
        Scrolls down the page by 2000 then calls get_links() and continues on to scroll for next 20 link elements
        whilst less then the maximum height of the page.
        '''
        max_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        scroll_down_y_axis = 2000

        while scroll_down_y_axis < max_page_height:
            self.driver.execute_script(f"window.scrollTo(0, {scroll_down_y_axis});")
            time.sleep(3)
            self.get_links()
            scroll_down_y_axis += 2000

def scraper():
    scraper = Scraper()
    time.sleep(2)
    scraper.accept_cookies()
    scraper.change_currency()
    #scraper.search_bar()
    scraper.scroll_bottom()
    scraper.data_scrape(coins_to_scrape = 3)
    # print(scraper.img_list)
    # print(len(scraper.img_list))
    # #print(scraper.img_name_list)
    #print(scraper.dict)
    #print(scraper.nested_dict)
    print(scraper.coin_data_dict)
    x = pd.DataFrame(scraper.coin_data_dict)
    print(x)
    exit()


if __name__ == '__main__':
    scraper()


