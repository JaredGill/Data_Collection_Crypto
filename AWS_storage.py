from msilib.schema import Class
from os.path import join
from dataclasses import asdict
from os import getcwd
from Scraper import CoinScraper
import json
import urllib.request
import boto3
import os
from sqlalchemy import create_engine
import pandas as pd

class AWS_Data_Storage(CoinScraper):
    
    def __init__(self):
        super().__init__()
        self.s3_client = boto3.client('s3')
        #self.s3_root_folder = join(dir_path, 'raw_data') if dir_path else 'raw_data'

    def upload_raw_data_dir_to_s3(dir_path: str = 'C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data', bucket: str = 'aicore-coinbucket'):
        s3 = boto3.client('s3')

        # using a path to the directory the os.walk function generates the file names in directory tree by walking up or down.
        # it gives a 3tuple(dirpath, dirnames, filenames)
        # root : Prints out directories only from what you specified.
        # dirs : Prints out sub-directories from root.
        # files : Prints out all files from root and directories.
        # Here the files is used to upload all raw data to bucket

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                #provides the file_name as the root path + the file name, bucketname, and object_name as the files existing name)
                s3.upload_file(os.path.join(root, file), bucket, file)


    def upload_tabular_data_to_RDS(self):
        #pip installed SQLAlchemy

        #("{type of database}+{DBAPI}://{username}:{password}@{host}:{port}/{database_name}")
        engine = create_engine('postgresql+psycopg2://postgres:MarbleArch@coindb.clip2s0923df.eu-west-2.rds.amazonaws.com:5432/coindb')
        tab_data = self.make_dataframe()
        try:
            tab_data.to_sql('coindb', engine, if_exists='append')
        except:
            print("Could not save df")

#os.environ1
#https://www.youtube.com/watch?v=IolxqkL7cD8

if __name__ == '__main__':
    AWS_Data_Storage.upload_raw_data_dir_to_s3()