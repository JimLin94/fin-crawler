# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime, timedelta
from configs.path import DOWNLOAD_PATH
from helpers._selenium import ClientSideCrawler
from configs.url import KRX
from helpers._pd import parse_html_to_excel

def kospi_spider():
    browser = ClientSideCrawler(KRX)
    driver = browser.driver

    try:
        # Click the Stock id.
        kospi_btn = driver.find_element_by_css_selector('input.schdate[value=STK]')
        kospi_btn.click()
        print('The radio button is clicked %s' % kospi_btn)

        # if next_date:
        _next_date = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
        date_input = driver.find_element_by_css_selector('.cal-area input.schdate')
        date_input.clear()
        date_input.send_keys(_next_date)

        # Click the search button.
        submit_btn = driver.find_element_by_css_selector('button.btn-board-search')
        submit_btn.click()

        # Download the xml.
        download_btn = driver.find_element_by_css_selector(
            'button.btn-board-download')
        download_btn.click()

        timeout = 5
        seconds = 0
        files = os.listdir(DOWNLOAD_PATH)

        while seconds < timeout:
            time.sleep(1)
            next_files = os.listdir(DOWNLOAD_PATH)

            print('Counting down %s' % seconds)

            if len(next_files) > len(files):
                print('Done. Please read the file in %s' % DOWNLOAD_PATH)
                driver.close()
            seconds += 1

        browser.tear_down()
    except Exception as inst:
        print('Error occurs while running TOPIX')
        print(inst)
        browser.tear_down()

if __name__ == '__main__':
    kospi_spider()
