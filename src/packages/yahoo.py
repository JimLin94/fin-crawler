from configs.url import YAHOO
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from helpers._mysql import PyMysql

TABLE_NAME = 'yahoo'

'''
在這邊加入Yahoo的股票代碼
範例
URL: https://finance.yahoo.com/quote/005930.KS?p=005930.KS
?p=股票代碼
'''
stock_ls = ['005930.KS']

def yahoo_spider():
    try:
        for stock_code in stock_ls:
            res = requests.get(YAHOO + stock_code)
            print('Request code %s' % stock_code)
            print('Request %s' % res.status_code)

            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.content, 'html.parser')
                target_cols = soup.select('#quote-summary > div table tbody tr:nth-child(6) td:nth-child(2)')
                updated_time = datetime.strftime(datetime.now(), '%Y%m%d')

                try:
                    target_split = target_cols[0].get_text().strip().split('-')
                    low = target_split[0].replace(' ', '').replace(',', '')
                    high = target_split[1].replace(' ', '').replace(',', '')
                    print('SPLIT %s %s' % (high, low))
                    print('Crawler by the date... %s', updated_time)

                    db_con_inst = PyMysql()
                    ''' 52 Week Range '''
                    db_con_inst.cursur.execute('''
                        CREATE TABLE IF NOT EXISTS %s (
                            company_code VARCHAR(255),
                            52_week_range_low FLOAT,
                            52_week_range_high FLOAT,
                            date DATE
                        ) CHARACTER SET utf8 ENGINE=INNODB;
                    ''' % TABLE_NAME)

                    db_con_inst.cursur.execute('''
                        SELECT * FROM %s WHERE date='%s'
                    ''' % (TABLE_NAME, updated_time))

                    has_data_existed = db_con_inst.cursur.fetchone()

                    if has_data_existed:
                        print('Date is parsed already %s' % updated_time)
                        return

                    query = 'INSERT INTO yahoo (`company_code`, `52_week_range_low`, `52_week_range_high`, `date`) VALUES (%s, %s, %s, %s)'

                    db_con_inst.cursur.executemany(query, [[stock_code, float(low), float(high), updated_time]])
                    db_con_inst.connection.commit()

                except ValueError as inst:
                    print(inst)
                    print('Parse the DOM error compant code %s' % stock_code)
    except ValueError as inst:
        print(inst)
        print('Parse the DOM error compant code %s' % stock_code)
