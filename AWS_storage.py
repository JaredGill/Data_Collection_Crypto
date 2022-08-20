from msilib.schema import Class
from os.path import join
from dataclasses import asdict
from os import getcwd
import numpy as np
#from Scraper import CoinScraper
import json
import urllib.request
import boto3
import os
from sqlalchemy import create_engine
import pandas as pd
from datetime import date
from pandasgui import show



class AWS_Data_Storage():
    
    #stop inheritance via coinscraper
    #def __init__(self):
        #self.s3_client = boto3.client('s3')
        #self.s3_bucket = boto3.bucket
        #self.s3_root_folder = join(dir_path, 'raw_data') if dir_path else 'raw_data'
        #directory path for saving

    def local_save(self, ):
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


    def make_dataframe(self, scraper_dict: dict):
        df = pd.DataFrame(scraper_dict)
        # df = df.applymap(lambda s:s.lower() if type(s) == str else s)
        return df

    def clean_dataframe(self, df):
        cols = ['CurrentPrice (£)', '24hrLowPrice (£)', '24hrHighPrice (£)', 'MarketCap (£)', 'FullyDilutedMarketCap (£)', 'Volume (£)', 'Volume/MarketCap', 
                'CirculatingSupply', 'MarketDominance (%)']
        df[cols] = df[cols].applymap(lambda s:s.lower() if type(s) == str else s)
        df[cols] = df[cols].replace({'\£':'', ',': '', '#': '', 'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '',
                                        'h': '', 'i': '', 'j': '', 'k': '', 'l': '', 'm': '', 'n': '', 'o': '', 'p': '',
                                        'q': '', 'r': '', 's': '', 't': '', 'u': '', 'v': '', 'w': '', 'x': '', 'y': '', 'z': '',
                                        '/': '', '%': '', ' ': '', '"': ''}, regex=True) 
        
        #cosmos has -- as its fdmc so convert this to NaN
        try:
            df['FullyDilutedMarketCap'] = df['FullyDilutedMarketCap'].replace('--', np.NaN)
        except:
            print("No NaN")
        
        df[cols] = df[cols].astype(float)
        show(df)
        print(df)
        print(df.dtypes)
        return df

    def upload_raw_data_dir_to_s3(dir_path: str = 'C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data', bucket: str = 'aicore-coinbucket'):
        s3 = boto3.client('s3')

        # using a path to the directory the os.walk function generates the file names in directory tree by walking up or down.
        # it gives a 3tuple(dirpath, dirnames, filenames)
        # root : Prints out directories only from what you specified.
        # dirs : Prints out sub-directories from root.
        # files : Prints out all files from root and directories.
        # Here the files is used to upload all raw data to bucket
        # str(os.chdir) + ('C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data') - concatenate raw data dir
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                #provides the file_name as the root path + the file name, bucketname, and object_name as the files existing name)
                s3.upload_file(os.path.join(root, file), bucket, file)
        #read in s3 files to a list, then check if filename is already there etc then continue

    def upload_tabular_data_to_RDS(self, input_df, table_name: str = 'total_coin_data'):
        #pip installed SQLAlchemy

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = 'coindb.clip2s0923df.eu-west-2.rds.amazonaws.com'
        USER = 'postgres'
        PASSWORD = 'MarbleArch'
        PORT = 5432
        DATABASE = 'postgres'
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        engine.connect()
        #engine = create_engine(f'postgresql+psycopg2://postgres:MarbleArch@coindb.clip2s0923df.eu-west-2.rds.amazonaws.com:5432/coindb')
        input_df.to_sql(table_name, engine, if_exists='replace')
        ##uuid and timestamp change everytime scraper is run


    def input_save_options():
        options_list = ["1", "2", "3"]
        while True:
            user_input = input('Choose your save option, input 1 for local save, 2 for RDS save, or 3 for both')
            if len(user_input) > 1 :
                print('Please, enter solely 1, 2 or 3')
            else:
                pass
        return user_input

    def data_save_option():
        pass










#os.environ1
#https://www.youtube.com/watch?v=IolxqkL7cD8
#make a file a dict with keys for password etc, then read json in init 

if __name__ == '__main__':
    test = AWS_Data_Storage()
#     AWS_Data_Storage.upload_raw_data_dir_to_s3()
    test.upload_tabular_data_to_RDS()




    #method for upload, and for local, if 3 do both etc

############################Method for reading saved .json files to the RDS 
    #Loads the current dates .json file into json object (dict of dicts)
        # current_date = date.today()
        # with open(f'./raw_data/total_data/{current_date}_total_data.json', 'r') as f:
        #     data = json.load(f)
        #     #print(data)
        # tab_data = pd.DataFrame(data)
        # try:
        #     tab_data.to_sql('total_coin_data', engine, if_exists='replace')
        # except:
        #     print("Could not save df")