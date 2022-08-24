import time
from Scraper import CoinScraper
#from AWS_storage import AWS_Data_Storage

if __name__ == '__main__':
    # bot = Scraper()
    # time.sleep(2)
    # bot.close_popup()
    # time.sleep(2)
    # bot.accept_cookies()
    # time.sleep(2)
    # bot.change_currency()
    # time.sleep(5)

    scraper = CoinScraper()
    
    time.sleep(2)
    #
    save_choice = scraper.arg_par()
    
    #scraper.s3_bucket()
    
    scraper.close_popup()
    scraper.accept_cookies()
    scraper.change_currency()
    #scraper.search_bar()
    scraper.scroll_bottom()
    scraper.data_scrape(3)
    #print(scraper.coin_data_dict)
    scraper.make_coin_df()
    scraper.make_image_df()
    
    #pass the save choice in to determine where to save data/images
    scraper.save_option(save_choice)

    exit()
