from backup import Scraper
import unittest

class ScraperTestCase(unittest.TestCase):

    def setUp(self):
        self.s = Scraper()
        self.url = "https://coinmarketcap.com/"
        
    def test_get_links(self):
        links = self.s.get_links()
        first_url = "https://coinmarketcap.com/currencies/bitcoin/"
        last_url = "https://coinmarketcap.com/currencies/multi-collateral-dai"
        length_urls = 12
        self.assertEqual(first_url, links[0])
        #as top 100 crytpos change daily, last url may fail
        self.assertEqual(last_url, links[99])
        self.assertEqual(length_urls, links.count())
        #unittest.main(argv=[''], verbosity=2, exit=False)
        #verbosity denotes detail of pass/fail
        #exit = false doesnt reset ipkernal
        #1st and last url, right lenthg and type
        
unittest.main(argv=[''], verbosity=2, exit=False)

#python-m unittest name