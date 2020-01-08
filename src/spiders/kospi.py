# -*- coding: utf-8 -*-
from helpers._selenium import ClientSideCrawler
from configs.url import KRX
from helpers._pd import parse_html_to_excel
import lxml.html
from datetime import datetime, timedelta

def kospi_spider():
    browser = ClientSideCrawler(KRX)
    driver = browser.driver
    # Click the Stock id.
    kospi_btn = driver.find_element_by_css_selector('input.schdate[value=STK]')
    kospi_btn.click()
    print('The radio button is clicked %s' % kospi_btn)

    # if next_date:
    _next_date = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
    date_input = driver.find_element_by_css_selector('.cal-area input.schdate')
    date_input.clear()
    date_input.send_keys(_next_date)

    # Download the xml
    download_btn = driver.find_element_by_css_selector(
        'button.btn-board-download')
    download_btn.click()

    # Wait for the fetching data and get the HTML table.
    browser.wait_for_element('tbody.CI-GRID-BODY-TABLE-TBODY tr')
    table_element = driver.find_element_by_css_selector(
        'div.CI-GRID-BODY-INNER')

    # Extract the table string and write to the excel file.
    table_element_string = table_element.get_attribute('innerHTML')
    table = lxml.html.fromstring(table_element_string)

    # print('The table founded %s' % lxml.html.tostring(table))
    pd = parse_html_to_excel(lxml.html.tostring(table), 'kospi.xlsx', _next_date)

    submit_btn = driver.find_element_by_css_selector('button.btn-board-search')
    submit_btn.click()

    driver.close()

if __name__ == '__main__':
    kospi_spider()
