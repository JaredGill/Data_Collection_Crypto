from msilib.schema import Class
from os.path import join
from dataclasses import asdict
from os import getcwd
import numpy as np
#from Scraper import CoinScraper
import argparse

import json
import urllib.request
import boto3
import os
from sqlalchemy import create_engine
import pandas as pd
from datetime import date
from pandasgui import show



class AWS_Data_Storage():
    
    def __init__(self):
        #must define parser here or inheritance will not find the attribute when called - AttributeError: 'CoinScraper' object has no attribute 'arg_par'
        self.parser = argparse.ArgumentParser()
        #self.s3_client = boto3.client('s3')
        #self.s3_bucket = boto3.bucket
        #self.s3_root_folder = join(dir_path, 'raw_data') if dir_path else 'raw_data'
        #directory path for saving

    def local_save_data(self, df):
        '''
        Makes a.json file for the combined dictionary storing all coins data.

        '''

        data_folder_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/total_data"
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)

        current_date = date.today()
        
        #try save json to dict of lists#############
        #local save will overwrite any existing file for the current day when run for more up-to-date prices
        df.to_json(f'./raw_data/total_data/{current_date}_total_data.json')
    
    def local_save_img(self, img_dict: dict):
        '''
        Makes an images directory saves each logos image .jpeg

        '''
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
        '''
        Converts a dict from parameter into a df.

        Parameters:
        ----------
        scraper_dict: dict
            Dict to be converted to df
        '''
        df = pd.DataFrame(scraper_dict)
        return df

    def clean_dataframe(self, df):
        '''
        Cleans the raw scraper data in df by converting all strings to lowercase, 
        then removing each letter with replace method in selected columns as 'cols', which are converted to floats.
        Also replaces possible no value tuples with NaN.

        Parameters:
        ----------
        df: dataframe
            The dataframe to clean
        '''
        cols = ['CurrentPrice (£)', '24hrLowPrice (£)', '24hrHighPrice (£)', 'MarketCap (£)', 'FullyDilutedMarketCap (£)', 'Volume (£)', 'Volume/MarketCap', 
                'CirculatingSupply', 'MarketDominance (%)']
        df[cols] = df[cols].applymap(lambda s:s.lower() if type(s) == str else s)
        df[cols] = df[cols].replace({'\£':'', ',': '', '#': '', 'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '',
                                        'h': '', 'i': '', 'j': '', 'k': '', 'l': '', 'm': '', 'n': '', 'o': '', 'p': '',
                                        'q': '', 'r': '', 's': '', 't': '', 'u': '', 'v': '', 'w': '', 'x': '', 'y': '', 'z': '',
                                        '/': '', '%': '', ' ': '', '"': ''}, regex=True) 
        
        #cosmos has -- as its fdmc so convert this to NaN
        try:
            df['FullyDilutedMarketCap (£)'] = df['FullyDilutedMarketCap (£)'].replace('--', np.NaN)
        except:
            print("No NaN")
        #show(df)
        df[cols] = df[cols].astype(float)
        #show(df)
        # print(df)
        # print(df.dtypes)
        return df

    def upload_raw_data_dir_to_s3(self, dir_path: str = 'C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data', bucket: str = 'aicore-coinbucket'):
        '''
        Obtains all files from a parent directory and uploads them to an s3 bucket if they are not present already.

        Parameters:
        ----------
        dir_path:
            Path to the parent directory, default set as the raw data directory
        bucket:
            Name of the s3 bucket files will upload to
        '''

        s3_files = []
        s3_paths = []

        # In order to get all files and paths from a parent directory, a nested loop must be used.
        # The first loop retrieves all files from root and directories, only from the directory specified in the dir_path parameter.
        # It then saves all file names to a list
        #[[j for j in range(5)] for i in range(5)]
        #https://deejaygraham.github.io/2020/01/17/for-loops-to-list-comprehensions/
        for root, dirs, files in os.walk(dir_path):
            #Use .extend here as .append gives a list of lists [[], ['1INCH_logo.jpeg', 'AAVE_logo.jpeg', etc]
            s3_files.extend(files)

            # The second loop saves the complete path for each file to a list.
            for file in files:
                s3_paths.append(os.path.join(root, file))

        s3 = boto3.client('s3')
        
        # zip function allows iteration for 2+ lists
        # As the both lists were saving from the same order in os.walk, all their positions in the list will match
        for (file, path) in zip(s3_files, s3_paths):
            s3_results = s3.list_objects_v2(Bucket = bucket, Prefix = file)
            if 'Contents' in s3_results:
                #print(path + file)
                #print("Key exists in the bucket.")
                continue
            else:
                print(path + file)
                print("Key doesn't exist in the bucket.")
                #provides the directory of file to upload, bucketname, and object_name as the files existing name)
                s3.upload_file(path, bucket, file)
        
        return s3_files, s3_paths


    def upload_tabular_data_to_RDS(self, input_df, table_name: str):
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
        # will update the table if run more than once on the same day 
        input_df.to_sql(table_name, engine, if_exists='replace')
        ##uuid and timestamp change everytime scraper is run

        #check creat_engine, connect, if df to sql is called once
        #integration test, create another rds and see if possible to pull across table
            # use ifexists, ifreplace etc 

    def arg_par(self):
        # argparse is a way of adding positonal or optional arguments to code when run in command line 
        self.parser.add_argument('--save',
                            choices = (1, 2, 3, 4, 5),
                            dest = 'save_options',
                            default = 5,
                            help='Choose where to save scraper data: 1 for Local Save, 2 for Local and s3 Bucket save, 3 for RDS df upload, 4 for all, or 5 for none.',
                            type = int,
                            nargs = 1
                            )
        args = self.parser.parse_args()
        print('Run file with -h to discover more save options. Current selection is %r.' % args.save_options)

        #sometimes it saves as a list instead of an int so below is how to retrieve the option either way
        if isinstance(args.save_options, int):
            self.user_choice = args.save_options
            # print(type(self.user_choice))
            # print('int')
            # print(self.user_choice)
        elif isinstance(args.save_options, list):
            self.user_choice = args.save_options[0]
            # print(type(self.user_choice))
            # print('list')
            # print(self.user_choice)
        return self.user_choice
    
   




#pipreqs for requirements.txt generation
# pipreqs pathtosaveposition

#os.environ1
#https://www.youtube.com/watch?v=IolxqkL7cD8
#make a file a dict with keys for password etc, then read json in init 


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