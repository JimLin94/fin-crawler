from configs.url import TWOTC
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import sys
from helpers._mysql import PyMysql
from packages import compare
from helpers.store_high_low import store_high_low
from helpers.cnyes_api import cnyes_api

TABLE_NAME = 'twotc'
TABLE_NAME_HIGHT_LOW = 'twotchl52'
HIGH_LOW_RECORD = 'twotc_hl52_record'

def twotc_spider():
    try:
        res = requests.get(TWOTC)
        print('Request %s' % res.status_code)

        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.content, 'html.parser')
            all_p = soup.select('table thead tr td')
            updated_time = datetime.strftime(datetime.now(), '%Y%m%d')

            for p in all_p:
                regex_time_string = re.match(r'資料日期:([0-9\/]+)', p.get_text())

                if regex_time_string:
                    groups = re.findall(r'[0-9\/]+', regex_time_string.group())
                    updated_time = groups[0]

            table = soup.select('table tbody tr')
            source = list()
            codes = list()

            for row in table:
                cols = row.select('td')

                if cols:
                    col_len = len(cols)
                    data = []

                    for idx in range(col_len):
                        current = cols[idx].get_text().strip()
                        is_exist = bool(current)

                        if not is_exist:
                            continue
                        if idx == 2:
                            current = current.replace(',', '')
                        if idx == 0:
                            codes.append(current)
                        data.append(current)

                    data.append(updated_time)
                    source.append(data)

        print('The length of the TWOTC data is %s' % len(source))
        print('Crawler by the date... %s', updated_time)

        db_con_inst = PyMysql()
        ''' 代號, 名稱, 發行仟股數, 收市價, 產業類別, 更新日期 '''
        db_con_inst.cursur.execute('''
            CREATE TABLE IF NOT EXISTS %s (
                code INT,
                name VARCHAR(255),
                volume INT,
                close_price FLOAT,
                industry VARCHAR(255),
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

        query = 'INSERT INTO twotc (`code`, `name`, `volume`, `close_price`, `industry`, `date`) VALUES (%s, %s, %s, %s, %s, %s)'

        db_con_inst.cursur.executemany(query, source)
        db_con_inst.connection.commit()

        high_low = cnyes_api(symbols = codes, date = updated_time)
        print('high_low %s' % high_low)
        compare.compare_hl(high_low, TABLE_NAME_HIGHT_LOW, datetime.strptime(updated_time, '%Y%m%d'), HIGH_LOW_RECORD)
        # Insert High-low 52 today after the comparison is done.
        store_high_low(TABLE_NAME_HIGHT_LOW, updated_time, high_low)
    except:
        e = sys.exc_info()[0]
        print(e)
        print('Parse the DOM error')
