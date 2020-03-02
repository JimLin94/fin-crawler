# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from configs.path import DOWNLOAD_PATH
from settings import WEB_DRIVER_HOST, WEB_DRIVER_PORT

CONNECTION_PATH = "http://%s:%s/wd/hub" % (WEB_DRIVER_HOST, WEB_DRIVER_PORT)

class ClientSideCrawler:
    def __init__(self, url, is_headless=False):
        options = Options()
        options.headless = is_headless
        options.add_argument('download.default_directory=' + DOWNLOAD_PATH)
        options.add_argument('--window-size=1360,768')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # self.driver = webdriver.Chrome(
        #     chrome_options=options, executable_path='http://%s:%s/wd/hub' % (WEB_DRIVER_HOST, WEB_DRIVER_PORT))
        self.driver = webdriver.Remote(
            desired_capabilities=options.to_capabilities(), command_executor="http://%s:%s/wd/hub" % (WEB_DRIVER_HOST, WEB_DRIVER_PORT))
        self.driver.get(url)

    def wait_for_element(self, css_selector):
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutError:
            print('Cannot find the element')

        return element

    def tear_down(self):
        self.driver.close()
        self.driver.quit()
