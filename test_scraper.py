import string
from typing_extensions import assert_type
from Scraper import CoinScraper
from Scraper import General_Scraper
import unittest
from unittest.mock import patch, Mock, call
import time
import pandas as pd
import json


class ScraperTestCase(unittest.TestCase):

    #setUP runs before every test
    def setUp(self):
        self.cs = CoinScraper()
        self.url = "https://coinmarketcap.com/"
    
    #tearDown runs after every test
    def tearDown(self):
        self.cs.driver.quit()
        del self.cs.driver
        return

    #When using patch to test methods being tested, it should be called in the class where it is used from, not where defined
    #Can mock any method such as time.sleep or send_keys
    #e.g. @patch('selenium.webdriver.remote.webelement.Webelement.send_keys')
    # @patch('Scraper.CoinScraper.get_links')
    # @patch('Scraper.CoinScraper.get_image')
    # @patch('Scraper.CoinScraper.get_text_data')
    def test_data_scrape(self, 
                        # mock_get_text_data: Mock, 
                        # mock_get_image: Mock, 
                        # mock_get_links: Mock
                        ):

        #pass 3 to method so it scrapes 3 different coins
        #self.cs.data_scrape(3)
        # mock_get_links.assert_called_once()

        # #mock_get_image.assert_has_calls(calls=)
        # image_call_count = mock_get_image.call_count
        # self.assertEqual(image_call_count, 3)

        # text_call_count = mock_get_text_data.call_count
        # self.assertEqual(text_call_count, 3)
        
        iterations = self.cs.data_scrape(3)
        number_of_coins = 3
        self.assertEqual(number_of_coins, iterations)
        self.assertIsInstance(iterations, int)


    def test_get_links(self):
        #get_links without scrolling only returns roughly the first 12 coin links
        links = self.cs.get_links()
        
        #1st and last url, right lenthg and type
        first_url = "https://coinmarketcap.com/currencies/bitcoin/"
        length_urls = 13
        self.assertEqual(first_url, links[0])
        #as top 100 crytpos change daily, last url may fail
        last_url = "https://coinmarketcap.com/currencies/shiba-inu/"
        self.assertEqual(last_url, links[11])
        self.assertEqual(length_urls, len(links))
        self.assertIsInstance(links, list)
    
    def test_get_image(self):
        #Dont want to call several methods to test this, instead give url to specific page
        self.cs.driver.get('https://coinmarketcap.com/currencies/bitcoin/')
        img = self.cs.get_image()
        #img = self.coin_data.get_image()
        url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/1.png'
        name = 'BTC'
        self.assertEqual(url, img[0])
        self.assertEqual(name, img[1])

    def test_get_text_data(self):
        # test_dict = {'CryptoName': ['Bitcoin (BTC)'], 'UUID': ['8d73b5b64315484eb6e8d1075cb0779a'], 'URL': ['https://coinmarketcap.com/currencies/bitcoin/'], 
        #             'CurrentPrice': ['Bitcoin Price £19,520.83'], '24hrLowPrice': ['£18,587.82 /'], '24hrHighPrice': ['£19,694.61'], 
        #             'MarketCap': ['Market Cap £373,614,210,638.43'], 'FullyDilutedMarketCap': ['Fully Diluted Market Cap £410,395,689,827.38'], 
        #             'Volume': ['£23,925,465,965.66'], 'Volume/MarketCap': ['Volume / Market Cap 0.06404'], 'CirculatingSupply': ['Circulating Supply 19,117,887 BTC'], 
        #             'MarketDominance (%)': ['Market Dominance 40.26%']}
        self.cs.driver.get('https://coinmarketcap.com/currencies/bitcoin/')

        data = self.cs.get_text_data()
        time.sleep(2)
        id_match = "Bitcoin (BTC)"
        self.assertEqual(id_match, data[0])

        #set up while loop to test all returns from get_text_data
        #i.e. the id_tag,  my_uuid, volume_tag, vol_mc_tag, price_tag, low_price_tag, high_price_tag, market_dom_tag, market_cap_tag, fdmc_tag, circ_supply_tag
        counter = 0
        list_counter = 0
        while counter < 10:
            self.assertIsInstance(data[list_counter], str)
            counter +=1
            list_counter +=1



    def test_local_save(self): 
        try: 
            with open('./raw_data/2022-08-14_total_data.json') as f: 
                return json.load(f) 
        except ValueError as e: 
            print('invalid json: %s' % e) 
            return None

    

    #mock responses, check if file exists, can convert josn to dict to check values(use assertequals)

unittest.main(argv=[''], verbosity=2, exit=False)
#verbosity denotes detail of pass/fail
#exit = false doesnt reset ipkernal


#python-m unittest name