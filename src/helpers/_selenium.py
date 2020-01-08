# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ClientSideCrawler:
    def __init__(self, url, is_headless = False):
        options = Options()
        options.headless = is_headless
        options.add_argument('--window-size=1360,768')
        options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=options, executable_path='/Users/jim/Apps/chromedriver')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(url)

    def wait_for_element(self, css_selector):
        try:
            element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutError:
            print('Cannot find the element')

        return element

    def tearDown(self):
        self.driver.close()

# if __name__ == "__main__":
#     unittest.main()
