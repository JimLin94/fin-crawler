# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ClientSideCrawler:
    def __init__(self, url):
        options = Options()
        options.headless = True
        # driver = webdriver.Chrome(chrome_options=options, executable_path='/Users/jim/Apps/chromedriver')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(url)

    def wait_for_element(self, css_selector):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except IOError:
            print('Cannot find the element')

        return element

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
