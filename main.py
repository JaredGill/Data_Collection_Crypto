import time
from Scraper import CoinScraper
import os
import env_vars

if __name__ == '__main__':
    
    scraper = CoinScraper()
    
    time.sleep(1)

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
    #print(CoinScraper.mro())
    
    #pass the save choice in to determine where to save data/images
    scraper.save_option(save_choice)

    exit()
