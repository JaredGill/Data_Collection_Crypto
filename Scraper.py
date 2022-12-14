from AWS_storage import AWS_Data_Storage 
from datetime import date
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import EdgeOptions
import pandas as pd
import numpy as np
import time
import uuid


class General_Scraper: 
    '''
    A general scraper class with methods that can be adapted and used for non-specific webpages.
    This class is one of two parent classes to the specific child CoinScraper class.
    In matters of inheritance it stands between the other parent class (AWS_Data_Storage) in the method resolution order.
    So this class had to inherit attributes to pass to the child class, hence the *args, and **kwargs

    Parameters:
    ----------
    URL: str
        The chosen websites url
    
    Attributes:
    ----------
    options: module
        Calls the class for managing specific options for selenium webdriver
    driver: module
        Calls the webdriver module to open a microsoft edge window
    delay: int
        Amount of time for the method webdriverwait to wait for xpaths to be present/load
    
    Methods:
    -------
    click_element()
        Finds and clicks a element 
    find_elements_in_container()
        Finds all elements in a given container and iterates through them
    close_popup()
        Closes a popup via specific xpaths
    accept_cookies()
        Closes cookies message
    change_currency()
        Changes the currency to the British Pound(£)
    scroll()
        Scrolls to input pixel height
    search_bar()
        Selects search bar and sends input text
    '''

    def __init__ (self, URL: str = "https://coinmarketcap.com/", *args, **kwargs):
        #args and kwargs let the class inherit any attributes to pass on to child class
        super().__init__(*args, **kwargs)

        #self denotes an attribute of the class, so its accessible to every other method of the class
        options = EdgeOptions()
        options.add_argument("--headless")

        #suppresses all warnings that aren't LOG_FATAL
        options.add_argument("--log-level=2")

        #set the window size so correct xpaths are present
        options.add_argument("--window-size=1815, 992")

        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Edge(options = options)

        #this increases the edge window to maximum screen size on monitor, so wont work if headless
        #self.driver.maximize_window()

        self.driver.get(URL)
        self.delay = 10
        
    #all defs are public
    def click_element(self, xpath: str):
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

    def find_elements_in_container(self, container_xpath: str, element_tag) -> list:
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
        
        Returns:
        -------
        test_obj
            Object is for unittest. If popup is closed then test_obj will be empty list.
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
                            ):
        '''
        Waits for the accept cookies element to appear then closes it.

        Parameters:
        ----------
        cookies_xpath: str
            The cookies element xpath.
        button_xpath: str
            The close cookies button xpath
        '''
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, cookies_xpath)))
            self.click_element(button_xpath)
            time.sleep(1)
        except TimeoutException:
            print("Cookies are automatically accepted when browsing coinmarket.")

    def change_currency(self):
        '''
        Opens the Select Currency button and selects British pound(GBP) when element is present.
        '''
        try:
            self.click_element('//button[@title="Select Currency"]')
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="de9tta-2 iemqlh cmc-modal-wrapper has-title "]')))
            time.sleep(2)
            self.click_element('//*[@class="ig8pxp-0 jaunlC"]')
        except:
            print("Currency already in GBP")

    def scroll(self, pixels_to_scroll_by: int = 2000):
        '''
        Scrolls to a specific height.

        Parameters:
        ----------
        pixels_to_scroll_by: int
            Amount of pixels to scroll by on the webpage
        '''
        try:
            self.driver.execute_script(f"window.scrollTo(0, {pixels_to_scroll_by});")
        except:
            print("Could not scroll to target pixel height.")

    def search_bar(self, text_search: str = "xrp"):
        '''
        Opens the search bar and inputs text via parameter then clicks.

        Parameters:
        text_search: str
            The desired text to be searched.
        
        Returns:
        -------
        get_url
            For unittest check the url of page is equal to expected url after sending keys
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
        
        get_url = self.driver.current_url
        return get_url


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
    img_dict: dict
        A dict of the image names and links.
    coin_data_dict: dict
        A dictionary of lists, each list containing the text data in order of market rank starting with bitcoin

    Methods:
    -------  
    get_link()
        Finds the links for each crytpo coin in the page
    data_scrape()
        Goes through each coin's link and scrapes data
    get_image()
        Finds the coin's logo in its page
    get_text_data()
        Locates and returns the text data on a coins unique page
    scroll_bottom()
        Scrolls to the bottom of the page
    make_coin_df()
        Converts coin_data_dict to df and cleans it.
    make_image_df()
        Converts img_dict to df.
    rds_upload()
        Uploads df's to AWS RDS
    save_option()
        Different options for save, dependant on arg par option.
    '''
    def __init__ (self, URL: str = "https://coinmarketcap.com/"):
        #super requires arguments(URL) as their part of parent classes constructor
        super().__init__(URL)
        self.img_dict = {"ImageName": [], "ImageLink": []}
        self.coin_data_dict = {'CryptoName': [], 'ShortName': [], 'UUID': [], 'URL': [], 'CurrentPrice (£)': [], '24hrLowPrice (£)': [], '24hrHighPrice (£)': [], 
                                'MarketCap (£)': [], 'FullyDilutedMarketCap (£)': [], 'Volume (£)': [], 'Volume/MarketCap': [], 
                                'CirculatingSupply': [], 'MarketDominance (%)': []}

    #public
    def get_links(self):
        '''
        Locates each unique coin in the main contianer on the homepage by "a" tag, and saves the href as a link.
        The link_list saves all hrefs that have loaded on page as website has dynamic pages.
        The url_list contains all unique hrefs from the link_list 

        Returns: 
        -------
        url_list
            List containing unique urls
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
    def data_scrape(self, coins_to_scrape = 0):
        '''
        Iterates through url_list by calling self.get_links() function for get_text_data() and get_image() to scrape.
        Appends the URL in use to the coin_data dictionary so the arrays are the same length.
        Calls get_text_data() in the while loop to add data for each coins url.

        Parameters:
        ----------
        coins_to_scrape: int
            Amount of crypto coins to be scraped

        Returns:
        -------
        url_counter
            Counter to test against how many urls were scraped through
        '''
        url_counter = 0
        coin_link_list = self.get_links()
    
        while url_counter < coins_to_scrape:
            URL = coin_link_list[url_counter]
            self.driver.get(URL)
            time.sleep(1)
            self.get_image()
            time.sleep(1)
            self.get_text_data()
            self.coin_data_dict['URL'].append(coin_link_list[url_counter])
            url_counter += 1

        return url_counter
        
    #public
    def get_image(self):
        '''
        Locates the coin's image logo by container, then returns its src and alt for img link and name respectively

        Returns:
        -------
        img_link
            Image link to be tested in unittest
        img_name
            Image name to be tested in unittest
        '''
        img_tag = self.find_elements_in_container('//div[@class="sc-16r8icm-0 gpRPnR nameHeader"]', 'img')
        img_link = img_tag.get_attribute('src')
        self.img_dict["ImageLink"].append(img_link)
        img_name = img_tag.get_attribute('alt')
        self.img_dict["ImageName"].append(img_name)
        
        return img_link, img_name

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

        # Get coin name and abbrevation.
        title = self.driver.find_element(by=By.XPATH, value='//h2[@class="sc-1q9q90x-0 jCInrl h1"]').text
        id_tag = title.replace('\n', ' (')
        split_name = id_tag.split(' (')
        self.coin_data_dict['CryptoName'].append(split_name[0])
        self.coin_data_dict['ShortName'].append(split_name[-1])
        
        # Scroll to show the necessary button for data scrape.
        time.sleep(1)
        self.scroll()
        time.sleep(2)
        
        # CoinMarket introduced new xpaths for specific coins.
        # Below are methods on how to find the button to show data for scraping.
        # First try except is the xpaths for ~95% of the coins:
        try:
            show_more_button = self.driver.find_element(by=By.XPATH, value='//div[@class="sc-16r8icm-0 sc-19zk94m-1 gRSJaB"]//div[@class="sc-19zk94m-4 eYCtRS"]//div[@class="sc-16r8icm-0 hgKnTV"]//div[@class="sc-16r8icm-0 nds9rn-0 cQtSIv"]//button[@class="x0o17e-0 dDXPcp"]')
            show_more_button.click()
        except:
            print("Current page has alt xpaths")
        
        try:
            show_more_button_alt = self.driver.find_element(by=By.XPATH, value='//div[@class="sc-16r8icm-0 sc-19zk94m-1 eToEXD"]//div[@class="sc-19zk94m-4 eYCtRS"]//div[@class="sc-16r8icm-0 hgKnTV"]//div[@class="sc-16r8icm-0 nds9rn-0 cQtSIv"]//button[@class="x0o17e-0 dDXPcp"]')
            show_more_button_alt.click()
        except:
            pass

        try:
            show_more_button_alt2 = self.driver.find_element(by=By.XPATH, value='//div[@class="sc-16r8icm-0 sc-19zk94m-1 cOhEUB"]//div[@class="sc-19zk94m-4 eYCtRS"]//div[@class="sc-16r8icm-0 hgKnTV"]//div[@class="sc-16r8icm-0 nds9rn-0 cQtSIv"]//button[@class="x0o17e-0 dDXPcp"]')
            show_more_button_alt2.click()
        except:
            pass

        time.sleep(1)
        
        #Here the elements of the container holding some of the desired data are found.
        try:
            data_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="sc-19zk94m-4 eYCtRS"]//div[@class="sc-16r8icm-0 iutcov"]//div[@class="sc-16r8icm-0 nds9rn-0 cQtSIv"]')
        except TimeoutException:
            print("fail")

        # Splits the list of scraped data by new lines.
        data_list = data_container[0].text.split('\n')

        # Appends to the dict the complimentary tags
        volume_tag = data_list[12]
        vol_mc_tag = data_list[14]
        self.coin_data_dict['Volume (£)'].append(volume_tag)
        self.coin_data_dict['Volume/MarketCap'].append(vol_mc_tag)

        # Coins such as yearn finance have string for price like 'yearn.finance Price $11,405.31'
        # This leave an extra "." in the float so to prevent this
        # split the full string by spaces then only append the position of the price
        price_split = data_list[2].split(' ')
        price_tag = price_split[-1]
        self.coin_data_dict['CurrentPrice (£)'].append(price_tag)

        low_price_tag = data_list[8]
        high_price_tag = data_list[9]
        market_dom_tag = data_list[15]
        circ_supply_tag = data_list[-4]
        self.coin_data_dict['24hrLowPrice (£)'].append(low_price_tag)
        self.coin_data_dict['24hrHighPrice (£)'].append(high_price_tag)
        self.coin_data_dict['MarketDominance (%)'].append(market_dom_tag)
        self.coin_data_dict['CirculatingSupply'].append(circ_supply_tag)

        # Some values are found in a seperate container.
        # This container can also change depending on the coin.
        # So the values are scraped depending on the size of elements found.
        values_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="statsValue"]')
        if len(values_container) == 5:
            market_cap_tag = values_container[0].text
            fdmc_tag = values_container[1].text
            self.coin_data_dict['MarketCap (£)'].append(market_cap_tag)
            self.coin_data_dict['FullyDilutedMarketCap (£)'].append(fdmc_tag)
        else:
            pass

        if len(values_container) == 7:
            market_cap_tag = values_container[0].text
            fdmc_tag = values_container[2].text
            self.coin_data_dict['MarketCap (£)'].append(market_cap_tag)
            self.coin_data_dict['FullyDilutedMarketCap (£)'].append(fdmc_tag)
        else:
            pass

        my_uuid = uuid.uuid4().hex
        self.coin_data_dict['UUID'].append(my_uuid)

        #cant return the self.coin_data_dict as it is used in other methods 
        return id_tag,  my_uuid, volume_tag, vol_mc_tag, price_tag, low_price_tag, high_price_tag, market_dom_tag, market_cap_tag, fdmc_tag, circ_supply_tag
 
    def scroll_bottom(self):
        '''
        Scrolls down the page by 2000 then calls get_links() and continues on to scroll for next 20 link elements
        whilst less then the maximum height of the page.
        '''
        max_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        scroll_down_y_axis = 2000

        while scroll_down_y_axis < max_page_height:
            self.scroll(scroll_down_y_axis)
            time.sleep(2)
            self.get_links()
            scroll_down_y_axis += 2000

    def make_coin_df(self):
        '''
        Makes a dataframe of total coin data scraped, then cleans it.

        Returns:
        -------
        clean_data_df
            Dataframe with cleaned total scraped coin data 
        '''
        data = super().make_dataframe(self.coin_data_dict)
        clean_data_df = super().clean_dataframe(data)
        
        return clean_data_df
    
    def make_image_df(self):
        '''
        Makes a dataframe for image name and url in dict

        Returns:
        -------
        image_df
            Dataframe with image name and url
        '''
        image_df = super().make_dataframe(self.img_dict)

        return image_df

    def rds_upload(self):
        '''
        Uploads the df's for the current day to AWS RDS.
        '''
        # set the date.today()to a variable as otherwise there will be an identifier error when naming table:
        # sqlalchemy.exc.IdentifierError: Identifier '<built-in method today of type object at 0x00007FFD5A970BF0>_data' exceeds maximum length of 63 characters 
        current_date = date.today()
        coin_df = self.make_coin_df()
        img_df = self.make_image_df()
        super().upload_tabular_data_to_RDS(coin_df, f'{current_date}_data')
        super().upload_tabular_data_to_RDS(img_df, 'coin_images')

    def save_option(self, choice: int):
        '''
        As crypto coin prices change constantly, the save file is named for the day scraper was ran.
        This is a method to decide how data will be saved:
            local_save_data will overwrite any file with the same day when run
            local_save_img will not save a image jpeg already present
            upload_raw_data_dir_to_s3() can only be run once a day as it will not update the bucket if rerun
                - So it is recommended to delete the old save file from s3 bucket for the date before running this 
            self.rds_upload() will update the rds table with new prices when ran
        
        Parameters:
        ----------
        choice: int
            The users choice for save options obtained from the arg_par method 

        '''
        coin_df = self.make_coin_df()
        
        if choice == 1:
            print('1111 - local save')
            super().local_save_data(coin_df)
            super().local_save_img(self.img_dict)
        elif choice == 2:
            print("2222 - local and s3 bucket save")
            super().local_save_data(coin_df)
            super().local_save_img(self.img_dict)
            super().upload_raw_data_dir_to_s3()
        elif choice == 3:
            print("3333 - upload to rds")
            self.rds_upload()
        elif choice == 4:
            print("4444 - local save, s3 bucket & rds upload")
            super().local_save_data(coin_df)
            super().local_save_img(self.img_dict)
            super().upload_raw_data_dir_to_s3()
            self.rds_upload()
        else:
            print("5555 - no save")
            pass
