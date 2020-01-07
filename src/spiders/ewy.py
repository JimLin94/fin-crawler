# -*- coding: utf-8 -*-
from helpers._selenium import ClientSideCrawler
from configs.url import KRX

def ewy_spider():
    browser = ClientSideCrawler(KRX)
    driver = browser.driver

    ewy_btn = driver.find_element_by_css_selector('input.schdate[value=STK]')
    ewy_btn.click()
    print('The radio button is clicked %s' % ewy_btn)

    table = browser.wait_for_element('tbody.CI-GRID-BODY-TABLE-TBODY')
    print('The table founded %s' % table)

    print('The table content is %s' % table.get_attribute('innerHTML'))

    submit_btn = driver.find_element_by_css_selector('button.btn-board-search')
    submit_btn.click()

    # driver.implicitly_wait(5)
    driver.close()

if __name__ == '__main__':
    ewy_spider()
