# -*- coding: utf-8 -*-
from helpers._selenium import ClientSideCrawler
from configs.url import KRX

def ewy_spider():
    browser = ClientSideCrawler(KRX)
    driver = browser.driver
    # Click the Stock id
    ewy_btn = driver.find_element_by_css_selector('input.schdate[value=STK]')
    ewy_btn.click()
    print('The radio button is clicked %s' % ewy_btn)
    # Wait for the fetching data and get the HTML
    browser.wait_for_element('tbody.CI-GRID-BODY-TABLE-TBODY')
    table = driver.execute_script('''
        var table = document.querySelector('tbody.CI-GRID-BODY-TABLE-TBODY');

        return table.innerHTML;
    ''')
    print('The table founded %s' % table)

    submit_btn = driver.find_element_by_css_selector('button.btn-board-search')
    submit_btn.click()

    # driver.implicitly_wait(5)
    driver.close()

if __name__ == '__main__':
    ewy_spider()
