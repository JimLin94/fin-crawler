# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import pandas as pd

from configs.url import N225
from helpers._pd import parse_html_to_excel
from helpers._mysql import df_insert_to_db, check_value_exist

TABLE_NAME = 'n225'

def n225_spider():
    res = requests.get(N225)
    print('Request %s' % res.status_code)

    if res.status_code == requests.codes.ok:
        soup = BeautifulSoup(res.content, 'html.parser')
        code_list = soup.select('.row.component-list > div')
        company_list = soup.select('.row.component-list > a')
        updated_time = soup.select('.last-update')
        today = datetime.strftime(datetime.now(), '%Y%m%d')
        source = []

        try:
            raw_updated_time_text = updated_time[0].get_text()
            updated_time_text = re.sub(r'^Update：', '', raw_updated_time_text)
            updated_time_form_instance = datetime.strptime(
                updated_time_text, '%b/%d/%Y')
            updated_time_form_text = updated_time_form_instance.strftime(
                '%Y/%m/%d')
            print('Crawler by the date... %s', updated_time_form_text)

            for idx in range(len(code_list)):
                source.append([code_list[idx].get_text(), company_list[idx].get_text(
                ), updated_time_form_text])
        except ValueError:
            print('Parse the DOM error')

    df = pd.DataFrame(source, columns=['Code', 'Company', 'Date'])

    try:
        is_duplicated = check_value_exist(
            'SELECT * FROM %s WHERE Date="%s"' % (TABLE_NAME, updated_time_form_text))

        if not is_duplicated:
            df_insert_to_db('%s' % TABLE_NAME, df)
    except Exception:
        print('Import to the database failed. Export to the excel instead')
        parse_html_to_excel(df, '%s.xlsx' % TABLE_NAME, today)
