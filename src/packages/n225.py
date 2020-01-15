# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from configs.url import N225
from helpers._pd import parse_html_to_excel

import pandas as pd


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
            updated_time_form_instance = datetime.strptime('Jan/15/2020', '%b/%d/%Y')
            updated_time_form_timestamp = updated_time_form_instance.timestamp()
            updated_time_form_text = updated_time_form_instance.strftime('%Y/%m/%d')

            print('Updated %s' % updated_time_form_instance.timestamp())

            for idx in range(len(code_list)):
                source.append([code_list[idx].get_text(), company_list[idx].get_text(
                ), updated_time_form_text, updated_time_form_timestamp])
        except ValueError:
            print('Parse the DOM error')

        # print('HTML %s %s' % (code_list, company_list))
    df = pd.DataFrame(source, columns=['Code', 'Company', 'Date', 'Timestamp'])

    print('DF %s' % df)
    parse_html_to_excel(df, 'n225.xlsx', today)
