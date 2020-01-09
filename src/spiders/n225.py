# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from configs.url import N225
import pandas as pd
from helpers._pd import parse_html_to_excel

def n225_spider():
    res = requests.get(N225)
    print('Request %s' % res.status_code)

    if res.status_code == requests.codes.ok:
        soup = BeautifulSoup(res.content, 'html.parser')
        code_list = soup.select('.row.component-list > div')
        company_list = soup.select('.row.component-list > a')
        today = datetime.strftime(datetime.now(), '%Y%m%d')
        source = []

        for idx in range(len(code_list)):
            source.append([code_list[idx].get_text(), company_list[idx].get_text()])

        # print('HTML %s %s' % (code_list, company_list))
    df = pd.DataFrame(source, columns=['Code', 'Company'])

    print('DF %s' % df)
    parse_html_to_excel(df, 'n225.xlsx', today)
