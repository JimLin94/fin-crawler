import sys
import requests
from configs.url import CNYES_API
import time
from datetime import datetime

def cnyes_api(symbols = [], market = 'TWS', date = datetime.strftime(datetime.now(), '%Y%m%d')):
    quotes = []
    counter = 0

    try:
        for symbol in symbols:
            time.sleep(1)
            url = '%s%s:%s:STOCK?column=G' % (CNYES_API, market, symbol)
            raw = requests.get(url)
            res = raw.json()
            data = res['data'][0]
            year_hight = data['3265']
            year_low = data['3266']
            quotes.append([symbol, year_low, year_hight, date])
        return quotes
    except:
        e = sys.exc_info()[0]
        print(e)

    return quotes

