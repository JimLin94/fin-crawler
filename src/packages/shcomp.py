from configs.url import SCHCOMP
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import sys
from helpers._mysql import PyMysql
from packages import yahoo, compare
from helpers.store_high_low import store_high_low

TABLE_NAME = 'shcomp'
TABLE_NAME_HIGHT_LOW = 'shcomphl52'
SHCOMP_SYMBOL_SUFFIX_IN_YAHOO_FINANCE = '.SS'

def shcomp_spider():
    try:
        res = requests.get(SCHCOMP, timeout=20)
        print('Request %s' % res.status_code)

        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.content, 'html.parser')
            rows = soup.select('#content_ab table tr td a')
            # rows = code_list.find_all('tr')

            updated_time = soup.select('#content_ab .tab_table_on')
            today = datetime.strftime(datetime.now(), '%Y%m%d')
            source = list()
            codes = list()

            raw_updated_time_text = updated_time[0].get_text()
            updated_time_text = re.sub('[^0-9]', '', raw_updated_time_text)
            print('updated_time_text__',
                  raw_updated_time_text, updated_time_text)

            updated_time_form_instance = datetime.strptime(
                updated_time_text, '%Y%m%d')
            updated_time_form_text = updated_time_form_instance.strftime(
                '%Y/%m/%d')
            yesterday_time = datetime.strftime(updated_time_form_instance - timedelta(1), '%Y%m%d')
            print('Crawler by the date... %s', updated_time_form_text)

            for idx in range(len(rows)):
                company_name = re.sub('[0-9\(\)\r\n\t]', '', rows[idx].get_text()).strip()
                code = re.sub('[^0-9]', '', rows[idx].get_text())
                source.append([company_name, code, updated_time_form_text])
                codes.append(code + SHCOMP_SYMBOL_SUFFIX_IN_YAHOO_FINANCE)

            db_con_inst = PyMysql()

            db_con_inst.cursur.execute('''
                CREATE TABLE IF NOT EXISTS %s (
                    company_name VARCHAR(255),
                    code INT,
                    date DATE
                ) CHARACTER SET utf8 ENGINE=INNODB;
            ''' % TABLE_NAME)

            db_con_inst.cursur.execute('''
                SELECT * FROM %s WHERE date='%s'
            ''' % (TABLE_NAME, source[0][2]))

            has_data_existed = db_con_inst.cursur.fetchone()

            if has_data_existed:
                print('Date is parsed already %s' % updated_time_form_text)
                return

            query = 'INSERT INTO shcomp (`company_name`, `code`, `date`) VALUES (%s, %s, %s)'

            db_con_inst.cursur.executemany(query, source)
            db_con_inst.connection.commit()

            high_low = yahoo.yahoo_spider(codes, TABLE_NAME_HIGHT_LOW, updated_time_form_text)
            print('high_low %s' % high_low)
            store_high_low(TABLE_NAME_HIGHT_LOW, updated_time_form_text, high_low)

            compare.compare_hl(high_low, TABLE_NAME_HIGHT_LOW, today)
            print('yesterday_time %s' % today)
    except:
        e = sys.exc_info()[0]
        print(e)
