import time
from Scraper import CoinScraper
from AWS_storage import AWS_Data_Storage

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
    aws_data = AWS_Data_Storage()
    time.sleep(2)
    scraper.close_popup()
    scraper.accept_cookies()
    scraper.change_currency()
    #scraper.search_bar()
    scraper.scroll_bottom()
    scraper.data_scrape(100)
    scraper.local_save()
    #s3_data.upload_raw_data_dir_to_s3()
    aws_data.upload_tabular_data_to_RDS()
    exit()
