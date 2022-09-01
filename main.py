import time
from Scraper import CoinScraper
import os
import env_vars

if __name__ == '__main__':
    
    scraper = CoinScraper()
    
    time.sleep(2)
    # AWS_SECRET_KEY = os.environ.get('AWS_Secret_Access_Key') 
    # AWS_ACCESS_KEY = os.environ.get('AWS_Access_Key')
    # AWS_REGION_NAME = "eu-west-2"

    # print(AWS_ACCESS_KEY)
    # print(AWS_REGION_NAME)
    # print(AWS_SECRET_KEY)
    save_choice = scraper.arg_par()
    
    
    scraper.close_popup()
    scraper.accept_cookies()
    scraper.change_currency()
    scraper.scroll_bottom()
    scraper.data_scrape(100)
    scraper.make_coin_df()
    scraper.make_image_df()
    print(scraper.make_coin_df())
    print(scraper.make_image_df())
    
    #pass the save choice in to determine where to save data/images
    scraper.save_option(save_choice)

    exit()
