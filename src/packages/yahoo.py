from configs.url import YAHOO_FINANCE
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from helpers._mysql import PyMysql

'''
在這邊加入Yahoo的股票代碼
範例
URL: https://finance.yahoo.com/quote/005930.KS
?p=股票代碼
'''
# stock_ls = ['005930.KS']

def yahoo_spider(source = [], table_name = '', updated_time = None):
    low_hight_collection = []
    counter = 0

    try:
        db_con_inst = PyMysql()
        ''' 52 Week Range '''
        db_con_inst.cursur.execute('''
            CREATE TABLE IF NOT EXISTS %s (
                company_code VARCHAR(255),
                52_week_range_low FLOAT,
                52_week_range_high FLOAT,
                date DATE
            ) CHARACTER SET utf8 ENGINE=INNODB;
        ''' % table_name)

        db_con_inst.cursur.execute('''
            SELECT * FROM %s WHERE date='%s'
        ''' % (table_name, updated_time))

        has_data_existed = db_con_inst.cursur.fetchone()

        if has_data_existed:
            print('Date is parsed already %s' % updated_time)
            return

        for stock_code in source:
            res = requests.get(YAHOO_FINANCE + stock_code)
            # print('Request %s %s' % (res.status_code, res.url))

            # counter += 1

            # if counter == 5:
            #     break

            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.content, 'html.parser')
                target_cols = soup.select('#quote-summary > div table tbody tr:nth-child(6) td:nth-child(2)')
                # updated_time = datetime.strftime(datetime.now(), '%Y%m%d')

                try:
                    target_split = target_cols[0].get_text().strip().split('-')
                    low = target_split[0].replace(' ', '').replace(',', '')
                    high = target_split[1].replace(' ', '').replace(',', '')
                    # print('Low, High %s %s' % (low, high))
                    # print('Crawler by the date... %s', updated_time)

                    low_hight_collection.append([stock_code, low, high, updated_time])
                except:
                    e = sys.exc_info()[0]
                    print(e)
                    print('Parse the DOM error compant code %s' % stock_code)
                    continue

        return low_hight_collection
    except:
        e = sys.exc_info()[0]
        print(e)
        print('Parse the DOM error compant code %s' % stock_code)
        return low_hight_collection
