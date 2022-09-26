import time
from Scraper import CoinScraper

if __name__ == '__main__':
    
    scraper = CoinScraper()
    
    time.sleep(1)

    # Initialise arg par for user if wanted.
    save_choice = scraper.arg_par()
    
    # Deal with unwanted elements of page and change currency to Pounds(£)
    scraper.close_popup()
    scraper.accept_cookies()
    scraper.change_currency()

    # Scroll through the page and scrape links
    scraper.scroll_bottom()

    # Scrape through a number of links for data
    scraper.data_scrape(100)

    # Make data into dataframes and clean
    scraper.make_coin_df()
    scraper.make_image_df()

    # Pass the save choice in to determine where to save data/images
    scraper.save_option(save_choice)

    exit()
