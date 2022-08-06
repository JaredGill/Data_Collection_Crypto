import time
from Scraper import Scraper


if __name__ == '__main__':
    bot = Scraper()
    time.sleep(2)
    bot.close_popup()
    time.sleep(2)
    bot.accept_cookies()
    time.sleep(2)
    bot.change_currency()
    time.sleep(5)
    