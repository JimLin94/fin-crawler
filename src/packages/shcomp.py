from configs.url import SCHCOMP
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from helpers._mysql import PyMysql

TABLE_NAME = 'shcomp'

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

            raw_updated_time_text = updated_time[0].get_text()
            updated_time_text = re.sub('[^0-9]', '', raw_updated_time_text)
            print('updated_time_text__',
                  raw_updated_time_text, updated_time_text)

            updated_time_form_instance = datetime.strptime(
                updated_time_text, '%Y%m%d')
            updated_time_form_text = updated_time_form_instance.strftime(
                '%Y/%m/%d')
            print('Crawler by the date... %s', updated_time_form_text)

            for idx in range(len(rows)):
                source.append([re.sub('[0-9\(\)\r\n\t]', '', rows[idx].get_text()).strip(), re.sub('[^0-9]', '', rows[idx].get_text()), updated_time_form_text])

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

    except ValueError as inst:
        print(inst)
        print('Parse the DOM error')
