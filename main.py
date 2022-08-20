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
    scraper.close_popup()
    scraper.accept_cookies()
    scraper.change_currency()
    #scraper.search_bar()
    scraper.scroll_bottom()
    scraper.data_scrape(3)
    print(scraper.coin_data_dict)
    print(scraper.img_dict)
    #datadf = scraper.make_dataframe()
    #scraper.local_save()
    scraper.data_handling()
    #print(scraper.img_dict)
    #s3_data.upload_raw_data_dir_to_s3()
    #scraper.upload_tabular_data_to_RDS(datadf)
    exit()
