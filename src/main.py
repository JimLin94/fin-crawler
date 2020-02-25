# -*- coding: utf-8 -*-
import schedule
import time
import sys
import requests
from packages import kospi, n225, topix
from settings import DB_HOST, DB_PORT, WEB_DRIVER_HOST, WEB_DRIVER_PORT

spider_name = sys.argv[1] if len(sys.argv) > 1 else False

request_jobs = {
    'n225': n225.n225_spider,
}

selenium_jobs = {
    # 'kospi': kospi.kospi_spider,
    # 'topix': topix.topix_spider,
}

def health_check(type):
    if type is 'db':
        res = requests.get('http://%s:%s' % (DB_HOST, DB_PORT))
        print('Request the DB is %s' % res.status_code)

        if res.status_code == requests.codes.ok:
            return True

    if type is 'webdriver':
        res = requests.get('http://%s:%s' % (WEB_DRIVER_HOST, WEB_DRIVER_PORT))
        print('Request the DB is %s' % res.status_code)

        if res.status_code == requests.codes.ok:
            return True

def request_crawler():
    request_status_ok = health_check('db')

    if request_status_ok:
        for k, v in request_jobs.items():
            print('Normal requesting Jobs...', v)
            v()
        schedule.every(12).hours.do(request_jobs['n225'])
    else:
        print('Cant connect to the DN')

def selenium_crawler():
    request_status_ok = health_check('webdriver')

    if request_status_ok:
        for k, v in request_jobs.items():
            print('Web Driver Jobs...', v)
            v()
        schedule.every(20).days.do(request_jobs['topix'])
    else:
        print('Cant connect to the DB')

def process():
    print('Launch the job...')
    jobs = {**request_jobs, **selenium_jobs}

    if spider_name:
        fn = jobs.get(spider_name, "The spider name not found.")
        fn()
    else:
        time.sleep(10)

        for k, v in jobs.items():
            print('Jobs...', v)
            v()
        # The source is updated daily.
        schedule.every(12).hours.do(jobs['n225'])
        # The source is updated monthly.
        # schedule.every(20).days.do(jobs['topix'])

        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    process()


if __name__ == '__main__':
    main()
