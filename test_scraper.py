from Scraper import CoinScraper
import unittest

class ScraperTestCase(unittest.TestCase):

    def setUp(self):
        self.s = CoinScraper()
        self.url = "https://coinmarketcap.com/"
        
    def test_get_links(self):
        #get_links without scrolling only returns first 12 coin links
        links = self.s.get_links()
        first_url = "https://coinmarketcap.com/currencies/bitcoin/"
        last_url = "https://coinmarketcap.com/currencies/multi-collateral-dai/"
        length_urls = 12
        self.assertEqual(first_url, links[0])
        #as top 100 crytpos change daily, last url may fail
        self.assertEqual(last_url, links[11])
        self.assertEqual(length_urls, len(links))
        self.assertIsInstance(links, list)
        
    def test_data_scrape(self):
        iterations = self.s.data_scrape()
        number_of_coins = 0
        self.assertEqual(number_of_coins, iterations)

    def test_get_text_data(self):
        data = self.s.get_text_data()
        id_match = "Tether (USDT)"
        self.assertEqual(id_match, data[0])


unittest.main(argv=[''], verbosity=2, exit=False)
#verbosity denotes detail of pass/fail
#exit = false doesnt reset ipkernal
#1st and last url, right lenthg and type

#python-m unittest name