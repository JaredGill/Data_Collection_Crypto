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
        length_urls = 17
        self.assertEqual(first_url, links[0])
        #as top 100 crytpos change daily, last url may fail
        last_url = "https://coinmarketcap.com/currencies/multi-collateral-dai/"
        #the amount of links scraped can very by 1 or 2 links so assertEqual may fail
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
        self.cs.driver.get('https://coinmarketcap.com/currencies/bitcoin/')
        data = self.cs.get_text_data()
        time.sleep(2)
        id_match = "Bitcoin (BTC"
        self.assertEqual(id_match, data[0])

        #set up while loop to test all returns from get_text_data
        #as these data points change constantly they are tested for type(string) not specific values
        #i.e. the id_tag,  my_uuid, volume_tag, vol_mc_tag, price_tag, low_price_tag, high_price_tag, market_dom_tag, market_cap_tag, fdmc_tag, circ_supply_tag
        counter = 0
        list_counter = 0
        while counter < 10:
            self.assertIsInstance(data[list_counter], str)
            counter +=1
            list_counter +=1

    @patch('AWS_storage.AWS_Data_Storage.clean_dataframe')
    @patch('AWS_storage.AWS_Data_Storage.make_dataframe')
    def test_make_coin_df(self,
                            mock_make_dataframe: Mock,
                            mock_clean_dataframe: Mock
                            ):
        self.cs.make_coin_df()
        mock_make_dataframe.assert_called_once()
        mock_clean_dataframe.assert_called_once()
        
    @patch('AWS_storage.AWS_Data_Storage.make_dataframe')
    def test_make_image_df(self,
                            mock_make_dataframe: Mock,
                            ):
        self.cs.make_image_df()
        mock_make_dataframe.assert_called_once()

    @patch('AWS_storage.AWS_Data_Storage.upload_tabular_data_to_RDS')
    @patch('Scraper.CoinScraper.make_image_df')
    @patch('Scraper.CoinScraper.make_coin_df')
    def test_rds_upload(self,
                            mock_make_coin_df: Mock,
                            mock_make_image_df: Mock,
                            mock_upload_tabular_data_to_RDS: Mock
                            ):
        self.cs.rds_upload()
        mock_make_coin_df.assert_called_once()
        mock_make_image_df.assert_called_once()
        mock_upload_tabular_data_to_RDS.assert_called()

    @patch('Scraper.CoinScraper.rds_upload')
    @patch('AWS_storage.AWS_Data_Storage.upload_raw_data_dir_to_s3')
    @patch('AWS_storage.AWS_Data_Storage.local_save_img')
    @patch('AWS_storage.AWS_Data_Storage.local_save_data')
    def test_save_option(self,
                            mock_local_save_data: Mock,
                            mock_local_save_img: Mock,
                            mock_upload_raw_data_dir_to_s3: Mock,
                            mock_rds_upload: Mock
                            ):
        #pass option 4 in to test if functions for data saved locally and uploaded to AWS S3 and RDS are called
        self.cs.save_option(4)
        mock_local_save_data.assert_called_once()
        mock_local_save_img.assert_called_once()
        mock_upload_raw_data_dir_to_s3.assert_called_once()
        mock_rds_upload.assert_called_once()


unittest.main(argv=[''], verbosity=2, exit=False)
#verbosity denotes detail of pass/fail
#exit = false doesnt reset ipkernal


#python-m unittest name