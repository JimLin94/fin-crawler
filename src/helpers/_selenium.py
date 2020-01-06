# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

class ClientSideCrawler:
    def __init__(self, url):
        self.driver = webdriver.Firefox()
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--hide-scrollbars')  # 隱藏滾動條, 應對一些特殊頁面
        firefox_options.add_argument(
            'blink-settings=imagesEnabled=false')  # 不載入圖片, 提升速度
        # 瀏覽器不提供視覺化頁面. linux下如果系統不支援視覺化不加這條會啟動失敗
        self.driver.get(url)

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
