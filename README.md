# Data_Collection_CoinMarket
Data scrape of the website https://coinmarketcap.com/ with Selenium to get crypto coin data.


##Building a Scraper 
- The package Selenium was used to open and control a webpage in Microsoft Edge to coinmarket using the code 
```python
def __init__ (self, URL: str = "https://coinmarketcap.com/"):
        self.driver = webdriver.Edge()
        self.driver.get(URL)
```
- Selenium finds specific features via xpaths, which can be found using ctrl + shift + c whilst on the webpage and hovering over elements.
- A unique xpath is preferred, or making a list of all elements found by xpath and choosing which to use.
- A common way to find unique xpaths is to obtain a parent xpath of element and set a variable equal to it called a container.
- In this container you can then refine the xpath search.
- Several methods were designed on this page to navigate it included accept cookies, change currency.
- Accept cookies waited for the element to appear on page then close the pop-up
```python
WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cmc-cookie-policy-banner"]')))
            self.accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@class="cmc-cookie-policy-banner__close"]')
            self.accept_cookies_button.click()
```
- Change currency finds and clicks option, waits for elements to load before clicking the british pound option.
```python
settings_button = self.driver.find_element(by=By.XPATH, value='//*[@class="sc-1pyr0bh-0 bSnrp sc-1g16avq-0 kBKzKs"]')
            settings_button.click()
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="vxp8h8-0 VMCHA"]')))
            select_currency_button = self.driver.find_element(by=By.XPATH, value='//button[@data-qa-id="button-global-currency-picker"]')
            select_currency_button.click()
            currency = self.driver.find_element(by=By.XPATH, value='//*[@class="ig8pxp-0 jaunlC"]')
            time.sleep(2)
            currency.click()
```
- Search bar method functions similarly to the above, but takes a string as parameter to input text.
- Scroll bottom finds the maximum height of the page then uses window.scrollTo() to descend by 2000
```python
max_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        scroll_down_y_axis = 2000

        while scroll_down_y_axis < max_page_height:
            self.driver.execute_script(f"window.scrollTo(0, {scroll_down_y_axis});")
            self.get_links()
            time.sleep(3)
            scroll_down_y_axis += 2000
```            

- In the above method there was a get_links() called. This method obtains the links for each coin via their "a" tag in the main container for the table on the homepage.
- It then saves the href's from the tags to a list.
```python 
self.coin_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="h7vnx2-1 bFzXgL"]//div[@class="sc-16r8icm-0 escjiH"]')
        for crypto_coin in self.coin_container:
            a_tag = crypto_coin.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
```
- As the website had dynamic pages, the page must scroll down to obtain the all the links.
    
## Retrieving Data and Images
- The method data_scrape() was created to iterate through unique links to travel to the coins pages and obtain relevant data.
- By passing in a number, you can look at the coins in order of their market rank descending from Bitcoin at rank #1
```python
url_counter = 0
        coin_link_list = self.get_links()
        
        while url_counter < coins_to_scrape:
            URL = coin_link_list[url_counter]
            self.driver.get(URL)
            self.get_image()
            self.get_text_data()
```
- In a While loop, two methods were called: get_image() and get_text_data().
- get_image() functioned similar to get_links working through a container, then finding image src for link/download, and alt for imgage name.
- get_text_data() also found some elements either by direct xpath, or container usage as well. But one container's data couldnt be refined to individual xpaths as all the class names were exactly the same. So instead the container located all elements and stored them in a list to be called upon as required.
```python
values_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="statsValue"]')
        self.coin_data_dict['MarketCap'].append(values_container[0].text)
        self.coin_data_dict['FullyDilutedMarketCap'].append(values_container[1].text)
        self.coin_data_dict['Volume'].append(values_container[2].text)
        self.coin_data_dict['Volume/MarketCap'].append(values_container[3].text)
        self.coin_data_dict['CirculatingSupply'].append(values_container[4].text)
```
- In addition a universally unique ID was generated using the UUID4 package.

pip3 freeze > requirements.txt was used to produce requirements.txt for docker

## Inheritance
The structure of the project was one child class (CoinScraper) inherits from two parent classes(General_Scraper and AWS_Data_Storage). This required several stapes:
- The method resolution order was found with cmd
```python 
        print(CoinScraper.mro())
```
- Which gave [<class 'Scraper.CoinScraper'>, <class 'Scraper.General_Scraper'>, <class 'AWS_storage.AWS_Data_Storage'>, <class 'object'>]
- The class on the left inherits from the previous two, similarly the class in the middle must inherit any attributes to be passed on.
- So both the left hand side, and middle class will have a super().__init__() in their __init__ method.
        - The General_Scraper class will have super().__init__(*args, **kwargs) to inherit and pass any arguements
    
## Environmental Variables
- Environmental variables were used to handle senstitive details for connecting to AWS RDS and S3.
- For the local windows machine this was done by searching and clicking "Edit the systems Environmental Variables".
        -Then selected the "Environmental variables option, and adding a new variable for AWS_Access_Key and AWS_Secret_Access_key
- For the EC2 Linux machine they were edited into the bottom of the bashrc file.
        - E.g. export AWS_ACCESS_KEY='example'
- These were called in the python script using the os.environ.get() function
- To pass these in the script when running the docker image they were called individually in the docker run line:
        - sudo docker run -it -e AWS_SECRET_KEY=$AWS_SECRET_KEY -e AWS_ACCESS_KEY=$AWS_ACCESS_KEY --name github_example jared22/crypto_scraper_repo
