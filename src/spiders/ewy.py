# -*- coding: utf-8 -*-
from helpers._selenium import ClientSideCrawler
from configs.url import KRX
import lxml.html

def ewy_spider():
    browser = ClientSideCrawler(KRX, True)
    driver = browser.driver
    # Click the Stock id
    ewy_btn = driver.find_element_by_css_selector('input.schdate[value=STK]')
    ewy_btn.click()
    print('The radio button is clicked %s' % ewy_btn)
    # Wait for the fetching data and get the HTML
    browser.wait_for_element('tbody.CI-GRID-BODY-TABLE-TBODY tr')
    table_element = driver.find_element_by_css_selector('tbody.CI-GRID-BODY-TABLE-TBODY')
    # table_element.screenshot('table.png')
    table_element_string = table_element.get_attribute('outerHTML')
    table = lxml.html.fromstring(table_element_string)

    # table = driver.execute_script('''
    # ''')
    print('The table founded %s' % lxml.html.tostring(table))

    submit_btn = driver.find_element_by_css_selector('button.btn-board-search')
    submit_btn.click()

    # driver.implicitly_wait(5)
    driver.close()

if __name__ == '__main__':
    ewy_spider()
