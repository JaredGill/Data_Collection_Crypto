from cgi import test
from AWS_storage import AWS_Data_Storage
import unittest
from unittest.mock import patch, Mock, call
from pathlib import Path
import pandas as pd
import numpy as np
import json
#import moto


class AWSTestCase(unittest.TestCase):

    def setUp(self):
        self.aws = AWS_Data_Storage()
    
    def tearDown(self) -> None:
        return

    def test_local_save_data(self): 
        try: 
            with open('./raw_data/total_data/2022-08-14_total_data.json') as f: 
                return json.load(f) 
        except ValueError as e: 
            print('invalid json: %s' % e) 
            return None

    def test_local_save_image(self):
        path_to_file = './raw_data/images/BTC_logo.jpeg'
        path = Path(path_to_file)
        path.is_file()
        
    def test_make_dataframe(self):
        test_dict = {}
        test_df = self.aws.make_dataframe(test_dict)
        test_df.empty

    def test_clean_dataframe(self):
        test_dict = {'CryptoName': ['Bitcoin'], 'ShortName': ['BTC'], 'UUID': ['411e71a4b0e54410bd6c2f24b5b5e903'], 
                    'URL': ['https://coinmarketcap.com/currencies/bitcoin/'], 'CurrentPrice (£)': ['£18,078.43'], 
                    '24hrLowPrice (£)': ['£17,682.20 /'], '24hrHighPrice (£)': ['£18,265.33'], 'MarketCap (£)': ['£345,834,428,023'], 
                    'FullyDilutedMarketCap (£)': ['£379,647,100,434'], 'Volume (£)': ['£27,658,400,933.19'], 
                    'Volume/MarketCap': ['Volume / Market Cap 0.07981'], 'CirculatingSupply': ['19,129,668.00 BTC'], 
                    'MarketDominance (%)': ['Market Dominance 39.83%']}
        test_df = pd.DataFrame(test_dict)
        test_clean_df = self.aws.clean_dataframe(test_df)
        cols = ['CurrentPrice (£)', '24hrLowPrice (£)', '24hrHighPrice (£)', 'MarketCap (£)', 'FullyDilutedMarketCap (£)', 
                'Volume (£)', 'Volume/MarketCap', 'CirculatingSupply', 'MarketDominance (%)']

        # Use of np.issubtdtype is due to the line in clean_dataframe: df[cols] = df[cols].astype(float)
        # This doesnt make a float object, instead it makes a dtype object 
        # which is an instance of numpys class dtype not Pythons class float
        np.issubdtype(test_clean_df[cols].dtypes, float)
        
    def test_upload_raw_data_dir_to_s3(self):
        test_path = 'C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data\images\AAVE_logo.jpeg'
        test_file_name = 'AAVE_logo.jpeg'
        method_lists = self.aws.upload_raw_data_dir_to_s3()
        file_list = method_lists[0]
        path_list = method_lists[1]
        self.assertEqual(path_list[1], test_path)
        self.assertEqual(file_list[1], test_file_name)
        #use moto to test s3 bucket
        

unittest.main(argv=[''], verbosity=2, exit=False)
