from ast import Str
from lib2to3.pgen2 import driver
from posixpath import split
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
from pandasgui import show
from datetime import date
from AWS_storage import AWS_Data_Storage 
import itertools
import pprint

class General_Scraper: 
    def __init__ (self, URL: str = "https://coinmarketcap.com/"):
        #self denotes an attribute of the class, so its accessible to every other method of the class
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.get(URL)
        self.delay = 10

    #all defs are public
    def click_element(self, xpath: str, *args):
        '''
        Locates and clicks a element on the webpage

        Parameters:
        ---------
        xpath: str
            The elements Xpath to be clicked
        '''
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            element.click()
        except:
            print('Could not click element. Are Xpaths correct?')

    def find_elements_in_container(self, container_xpath: str, element_tag, *args) -> list:
        '''
        General method to find elements in a container, then iterate through them

        Parameters: 
        ----------
        container_xpath: str
            The xpath of container
        element_tag: str
            The tag of desired element
        '''
        try:
            container = self.driver.find_elements(By.XPATH, container_xpath)
            for element in container:
                elements_in_container = element.find_element(By.XPATH, f'./{element_tag}')
                return elements_in_container
        except:
            print('Could not find elements in container. Are Xpaths correct?')
    
    def close_popup(self, popup_xpath: str = '//div[@class="sc-8ukhc-2 iCMWiP"]', 
                            popup_button_xpath: str = '//div[@class="gv-close"]',
                            *args):
        '''
        Closes any popup unwanted on webpage by waiting on the element then clicking relative close button through xpaths.

        Parameters:
        ---------
        popup_xpath: str
            The popup xpath
        popup_button_xpath: str
            The xpath for close button on popup
        '''
        time.sleep(1)
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, popup_xpath)))
            self.click_element(popup_button_xpath)
            time.sleep(1)
            #find_elements here -> if element no longer exists an empty list will be returned   
        except:
            print('Could not close popup. Is it present? Are Xpaths correct?')
        test_obj = self.driver.find_elements(by=By.XPATH, value=popup_button_xpath)
        #print(test_obj)
        return test_obj

    def accept_cookies(self, cookies_xpath: str = '//*[@id="cmc-cookie-policy-banner"]', 
                            button_xpath: str = '//*[@class="cmc-cookie-policy-banner__close"]',
                            *args):
        '''
        Waits for the accept cookies element to appear then closes it.
        '''
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, cookies_xpath)))
            self.click_element(button_xpath)
            time.sleep(1)
        except TimeoutException:
            print("Cookies are automatically accepted when browsing coinmarket.")

    #maybe change to have 3 letter currency in parameters and pass it in
    def change_currency(self, *args):
        '''
        Opens the Select Currency button and selects British pound(GBP) when element is present.
        '''
        try:
            self.click_element('//button[@title="Select Currency"]')
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="de9tta-2 iemqlh cmc-modal-wrapper has-title "]')))
            time.sleep(2)
            self.click_element('//*[@class="ig8pxp-0 jaunlC"]')

            ####If self.driver.maximize_window() is below self.driver.get(URL) in init method, page layout changes and below is how to change currency
            # self.click_element('//*[@class="sc-1pyr0bh-0 bSnrp sc-1g16avq-0 kBKzKs"]')
            # WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="vxp8h8-0 VMCHA"]')))
            # self.click_element('//button[@data-qa-id="button-global-currency-picker"]')
            # self.click_element('//*[@class="ig8pxp-0 jaunlC"]')

        except:
            print("Currency already in GBP")

    def scroll(self, pixels_to_scroll_by: int = 2000):
        try:
            self.driver.execute_script(f"window.scrollTo(0, {pixels_to_scroll_by});")
        except:
            print("Could not scroll to target pixel height.")

    def search_bar(self, text_search: Str = "xrp"):
        '''
        Opens the search bar and inputs text via parameter then clicks.

        Parameters:
        text_search: str
            The desired text to be searched.
        '''
        try:
            self.close_popup()
        except:
            pass

        #use find_elements instead of line 130 to return list to unittest
        #return current url and test
        try:
            search_bar = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="zafg3t-1 gaWePq"]')))
            search_bar.click()
        except:
            print('No element located, check xpath')

        time.sleep(2)
        active_element = self.driver.switch_to.active_element
        while True:
            try: 
                active_element.send_keys(text_search)
                time.sleep(2)
                active_element.send_keys(Keys.RETURN)
            except: 
                break
        
        #for unittest check the url of page is equal to expected url after sending keys
        get_url = self.driver.current_url
        return get_url


#multiple inheritance from aws storage
class CoinScraper(General_Scraper, AWS_Data_Storage):
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
        #maybe look into kwargs
        General_Scraper.__init__(self) # or super().__init__()  --> allows for dependency injection
        AWS_Data_Storage.__init__(self) # or super(General_Scraper, self).__init__()
        #super().__init__
        self.img_dict = {"ImageName": [], "ImageLink": []}
        self.coin_data_dict = {'CryptoName': [], 'ShortName': [], 'UUID': [], 'URL': [], 'CurrentPrice (£)': [], '24hrLowPrice (£)': [], '24hrHighPrice (£)': [], 
                                'MarketCap (£)': [], 'FullyDilutedMarketCap (£)': [], 'Volume (£)': [], 'Volume/MarketCap': [], 
                                'CirculatingSupply': [], 'MarketDominance (%)': []}
        self.df_to_dict = {}


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
        #print(coin_link_list)
        print(len(coin_link_list))
        while url_counter < coins_to_scrape:
            URL = coin_link_list[url_counter]
            self.driver.get(URL)
            time.sleep(1)
            self.get_image()
            time.sleep(1)
            self.get_text_data()
            self.coin_data_dict['URL'].append(coin_link_list[url_counter])
            #best to try upload to cloud as the loop continues so if there is an error it is obvious
            url_counter += 1
        return url_counter
        

    #public
    #put link into parameter for testing
    def get_image(self):
        '''
        Locates the coin's image logo by container, then returns its src and alt for img link and name respectively
        '''

        img_tag = self.find_elements_in_container('//div[@class="sc-16r8icm-0 gpRPnR nameHeader"]', 'img')
        img_link = img_tag.get_attribute('src')
        self.img_dict["ImageLink"].append(img_link)
        img_name = img_tag.get_attribute('alt')
        self.img_dict["ImageName"].append(img_name)
        
        return img_link, img_name

#put link into parameter for testing
    def get_text_data(self):
        '''
        Scrapes the data from the coin's specific webpage and appending them to the coin_data dictionary.
        This method is called in each iteration of the data_scrape method to populate the dictionary
        with each coins data.
        Price, 24hr low and high, MarketCap, FullyDilutedMarketCap, Volume, Volume/MarketCap, 
        CirculatingSupply, MarketRank and Dominance are found in the same container and using .text at specific positions 
        in the containers list. 
        ID is found directly calling the unique class xpath.
        
        A UUID was also generated using the package.
        '''

        title = self.driver.find_element(by=By.XPATH, value='//h2[@class="sc-1q9q90x-0 jCInrl h1"]').text
        id_tag = title.replace('\n', ' ')
        # id_tag = title.replace('\n', ' (') + ")"
        split_name = id_tag.split(' ')
        #print(split_name)
        self.coin_data_dict['CryptoName'].append(split_name[0])
        self.coin_data_dict['ShortName'].append(split_name[1])

        time.sleep(1)
        self.scroll()
        time.sleep(2)
        show_more_button = self.driver.find_elements(by=By.XPATH, value='//div[@class="sc-19zk94m-4 eYCtRS"]//div[@class="sc-16r8icm-0 iutcov"]//div[@class="sc-16r8icm-0 nds9rn-0 dAxhCK"]')

        for button in show_more_button:
            sh = button.find_element(by=By.XPATH, value='button')
            sh.click()

        try:
            data_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="sc-19zk94m-4 eYCtRS"]//div[@class="sc-16r8icm-0 iutcov"]//div[@class="sc-16r8icm-0 nds9rn-0 dAxhCK"]')
        except TimeoutException:
            print("fail")

        data_list = data_container[0].text.split('\n')

        volume_tag = data_list[12]
        vol_mc_tag = data_list[14]
        self.coin_data_dict['Volume (£)'].append(volume_tag)
        self.coin_data_dict['Volume/MarketCap'].append(vol_mc_tag)

        #coins such as yearn finance have string for price like 'yearn.finance Price $11,405.31'
        #this leave an extra "." in the float so to prevent this
        #split the full string by spaces then only append the position of the price
        price_split = data_list[2].split(' ')
        price_tag = price_split[-1]
        #print(x[2])s
        self.coin_data_dict['CurrentPrice (£)'].append(price_tag)

        low_price_tag = data_list[8]
        high_price_tag = data_list[9]
        market_dom_tag = data_list[15]
        self.coin_data_dict['24hrLowPrice (£)'].append(low_price_tag)
        self.coin_data_dict['24hrHighPrice (£)'].append(high_price_tag)
        self.coin_data_dict['MarketDominance (%)'].append(market_dom_tag)

        values_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="statsValue"]')
        if len(values_container) == 5:
            market_cap_tag = values_container[0].text
            fdmc_tag = values_container[1].text
            circ_supply_tag = values_container[4].text
            self.coin_data_dict['MarketCap (£)'].append(market_cap_tag)
            self.coin_data_dict['FullyDilutedMarketCap (£)'].append(fdmc_tag)
            self.coin_data_dict['CirculatingSupply'].append(circ_supply_tag)
        else:
            pass
        if len(values_container) == 7:
            market_cap_tag = values_container[0].text
            fdmc_tag = values_container[2].text
            circ_supply_tag = values_container[-1].text
            self.coin_data_dict['MarketCap (£)'].append(market_cap_tag)
            self.coin_data_dict['FullyDilutedMarketCap (£)'].append(fdmc_tag)
            self.coin_data_dict['CirculatingSupply'].append(circ_supply_tag)
        else:
            pass

        my_uuid = uuid.uuid4().hex
        self.coin_data_dict['UUID'].append(my_uuid)

        ##################
        #timestamp column
    
    #return the dict intead and test each column
        return id_tag,  my_uuid, volume_tag, vol_mc_tag, price_tag, low_price_tag, high_price_tag, market_dom_tag, market_cap_tag, fdmc_tag, circ_supply_tag

#can test xpath, whether valid or not, can mock find_element

   # def make_dataframe(self, dict: dict) -> pd.DataFrame:
   #class data_clean():
   #one instance in main class
    # def make_dataframe(self):
    #     df = pd.DataFrame(self.coin_data_dict)
    #     # df = df.applymap(lambda s:s.lower() if type(s) == str else s)

    #     cols = ['CurrentPrice', '24hrLowPrice', '24hrHighPrice', 'MarketCap', 'FullyDilutedMarketCap', 'Volume', 'Volume/MarketCap', 
    #             'CirculatingSupply', 'MarketDominance (%)']
    #     df[cols] = df[cols].applymap(lambda s:s.lower() if type(s) == str else s)
    #     df[cols] = df[cols].replace({'\£':'', ',': '', '#': '', 'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '',
    #                                     'h': '', 'i': '', 'j': '', 'k': '', 'l': '', 'm': '', 'n': '', 'o': '', 'p': '',
    #                                     'q': '', 'r': '', 's': '', 't': '', 'u': '', 'v': '', 'w': '', 'x': '', 'y': '', 'z': '',
    #                                     '/': '', '%': '', ' ': '', '"': ''}, regex=True) 
        
    #     #cosmos has -- as its fdmc so convert this to NaN
    #     df['FullyDilutedMarketCap'] = df['FullyDilutedMarketCap'].replace('--', np.NaN)
        
    #     df[cols] = df[cols].astype(float)
    #     show(df)
    #     print(df)
    #     print(df.dtypes)
    #     return df

#make raw json first then read into df, clean then convert back

    def local_save(self):
        '''
        Makes a.json file for the combined dictionary storing all coins data.
        Also makes an images directory saves each logos image .jpeg
        '''

        data_folder_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/total_data"
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)

        current_date = date.today()
        df = self.make_dataframe()
        #try save json to dict of lists#############
        df.to_json(f'./raw_data/total_data/{current_date}_total_data.json')

        image_folder_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/images"
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)
        
        img_name_list = self.img_dict["ImageName"]
        img_link_list = self.img_dict["ImageLink"]

        # zip function allows iteration for 2+ lists and runs until smallest list ends
        for (name, link) in zip(img_name_list, img_link_list):
            if not os.path.exists(f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/images/{name}_logo.jpeg"):
                image_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/images/{name}_logo.jpeg"
                urllib.request.urlretrieve(link, image_path)

    def scroll_bottom(self):
        '''
        Scrolls down the page by 2000 then calls get_links() and continues on to scroll for next 20 link elements
        whilst less then the maximum height of the page.
        '''
        max_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        scroll_down_y_axis = 2000

        while scroll_down_y_axis < max_page_height:
            #self.driver.execute_script(f"window.scrollTo(0, {scroll_down_y_axis});")
            self.scroll(scroll_down_y_axis)
            time.sleep(2)
            self.get_links()
            scroll_down_y_axis += 2000


####################################################TO DO LIST #############################################
#call everything into scraper for data, saving etc
#setup rds method
#file path details method
# link the data and img dicts, by splitting the name, removing the brackets from (BTC) and making a new column for it
    #   this new column is equal to the img name column in img dict
# img dict should be a table in rds
#have the user decide what to save through arguement parser from cmd line
    #   so they will decide e.g. 'l' for local save, 'r' for rds save, and 'b' for both or 'n' for neither

    def data_handling(self):
        data = self.make_dataframe(self.coin_data_dict)
        clean_data_df = self.clean_dataframe(data)
        #show(data)
        image_df = self.make_dataframe(self.img_dict)
        show(image_df)
        return clean_data_df, image_df

    #def 
        self.upload_tabular_data_to_RDS(data)
        self.upload_tabular_data_to_RDS(image, 'coin_images')




def scraper():
    scraper = CoinScraper()
    time.sleep(2)
    scraper.close_popup()
    scraper.accept_cookies()
    scraper.change_currency()
    scraper.scroll_bottom()
    scraper.data_scrape(1)
    # scraper.make_dataframe()
    #scraper.local_save()
    #pprint.pprint(scraper.coin_data_dict)
    print(scraper.mro())
    exit()


if __name__ == '__main__':
    scraper()
