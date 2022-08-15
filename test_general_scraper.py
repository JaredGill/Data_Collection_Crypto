from typing_extensions import assert_type
from Scraper import General_Scraper
import unittest
from unittest.mock import patch, Mock, call
import time

class ScraperTestCase(unittest.TestCase):

    #setUP runs before every test
    def setUp(self):
        self.s = General_Scraper()
        self.url = "https://coinmarketcap.com/"
    
    #tearDown runs after every test
    def tearDown(self):
        self.s.driver.quit()
        del self.s.driver
        return

    #right click and select "Go to definition" to see where the mehtod has been clicked in selenium
    @patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
    #@patch('selenium.webdriver.remote.webelement.WebElement.click')
    def test_click_element(self,
                            #mock_click_element: Mock,
                            mock_find_element: Mock):

        self.s.click_element('//div[@class="gv-close"]')
        mock_find_element.assert_called_once()
        #mock_click_element.assert_called_once()

    
    # @patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
    # @patch('selenium.webdriver.remote.webdriver.WebDriver.find_elements')
    # def test_find_elements_in_container(self,
    #                         mock_find_elements: Mock,
    #                         mock_find_element: Mock):

    #     element_tags = self.s.find_elements_in_container()
    #     mock_find_elements.assert_called_once()
    #     mock_find_element.assert_called_once()
    #     self.assertIsInstance(element_tags, list)

    @patch('selenium.webdriver.support.wait.WebDriverWait.until')
    @patch('selenium.webdriver.remote.webelement.WebElement.click')
    def test_close_popup(self,
                            mock_click_element: Mock,
                            mock_until: Mock):

        self.s.close_popup()
        time.sleep(2)
        mock_until.assert_called_once()
        mock_click_element.assert_called_once()
        
    @patch('selenium.webdriver.support.wait.WebDriverWait.until')
    @patch('selenium.webdriver.remote.webelement.WebElement.click')
    def test_accept_cookies(self,
                            mock_click_element: Mock,
                            mock_until: Mock):

        self.s.accept_cookies()
        mock_until.assert_called_once()
        mock_click_element.assert_called_once()

    @patch('selenium.webdriver.support.wait.WebDriverWait.until')
    @patch('Scraper.General_Scraper.click_element')
    def test_change_currency(self,
                            mock_click_element: Mock,
                            mock_until: Mock):

        self.s.change_currency()
        mock_until.assert_called_once()
        click_count = mock_click_element.call_count
        self.assertEqual(click_count, 2)

    @patch('selenium.webdriver.remote.webdriver.WebDriver.execute_script')
    def test_scroll(self,
                    mock_execute_script: Mock):
        self.s.scroll()
        mock_execute_script.assert_called_once()

    # @patch('selenium.webdriver.support.wait.WebDriverWait.until')
    # @patch('selenium.webdriver.remote.webelement.WebElement.click')
    # def test_search_bar(self,
    #                     mock_click_element: Mock,
    #                     mock_until: Mock):
        
    #     self.s.search_bar()
    #     until_count = mock_until.call_count
    #     self.assertEqual(until_count, 2)
    #     click_count = mock_click_element.call_count
    #     self.assertEqual(click_count, 2)
    

unittest.main(argv=[''], verbosity=2, exit=False)
