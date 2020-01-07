# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

class ClientSideCrawler:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        options = Options()
        options.headless = True
        # driver = webdriver.Chrome(chrome_options=options, executable_path='/path/to/chromedriver')

    def wait(self, delay = 5):
        self.driver.implicitly_wait(delay)
    # def crawl_url(self, url):
    #     driver = self.driver
    #     driver.get(url)
    #     # elem = driver.find_element_by_name("q")
    #     # elem.send_keys("pycon")
    #     # elem.send_keys(Keys.RETURN)
    #     # assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()

# if __name__ == "__main__":
#     unittest.main()
