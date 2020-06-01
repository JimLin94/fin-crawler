# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd
import sys

from configs.url import N225
from helpers._pd import parse_html_to_excel
from helpers._mysql import df_insert_to_db, check_value_exist, run_query
from settings import DB_NAME
from packages import yahoo, compare
from helpers.store_high_low import store_high_low

TABLE_NAME = 'n225'
TABLE_NAME_HIGHT_LOW = 'n225hl52'
N225_SYMBOL_SUFFIX_IN_YAHOO_FINANCE = '.T'
HIGH_LOW_RECORD = 'n225_hl52_record'

def n225_spider():
    try:
        res = requests.get(N225)
        print('Request %s' % res.status_code)

        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.content, 'html.parser')
            code_list = soup.select('.row.component-list > div')
            company_list = soup.select('.row.component-list > a')
            updated_time = soup.select('.last-update')
            source = []

            raw_updated_time_text = updated_time[0].get_text()
            updated_time_text = re.sub(r'^Update：', '', raw_updated_time_text)
            updated_time_form_instance = datetime.strptime(
                updated_time_text, '%b/%d/%Y')
            updated_time_form_text = updated_time_form_instance.strftime(
                '%Y/%m/%d')
            print('Crawler by the date... %s', updated_time_form_text)

            for idx in range(len(code_list)):
                source.append([code_list[idx].get_text() + N225_SYMBOL_SUFFIX_IN_YAHOO_FINANCE, company_list[idx].get_text(
                ), updated_time_form_text])

            df = pd.DataFrame(source, columns=['Code', 'Company', 'Date'])
            df_insert_to_db(table_name=TABLE_NAME, df=df,
                            check_value_column_name='Date', check_value=updated_time_form_text)
            high_low = yahoo.yahoo_spider(df['Code'], TABLE_NAME_HIGHT_LOW, updated_time_form_text)
            compare.compare_hl(high_low, TABLE_NAME_HIGHT_LOW, updated_time_form_instance, HIGH_LOW_RECORD)
            # Insert High-low 52 today after the comparison is done.
            store_high_low(TABLE_NAME_HIGHT_LOW, updated_time_form_text, high_low)
    except Exception as inst:
        print('Error occurs %s' % inst)
