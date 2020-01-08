# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime, timedelta
from configs.url import N225
from helpers._pd import parse_html_to_excel
from helpers._pd import parse_html_to_excel


def n225_spider():
    html_df = pd.read_html(N225)
    _next_date = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')

    print('HTML %s' % html_df)

    parse_html_to_excel(html_df, 'n225.xlsx', _next_date)
