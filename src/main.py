# -*- coding: utf-8 -*-
import schedule
import time
import sys
import requests
from packages import kospi, n225, topix, shcomp, taifex, twotc
from settings import DB_HOST, DB_PORT, WEB_DRIVER_HOST, WEB_DRIVER_PORT

spider_name = sys.argv[1] if len(sys.argv) > 1 else False

request_jobs = {
    'n225': n225.n225_spider,
    'shcomp': shcomp.shcomp_spider,
    'taifex': taifex.taifex_spider,
    'twotc': twotc.twotc_spider,
}

selenium_jobs = {
    'kospi': kospi.kospi_spider,
    'topix': topix.topix_spider,
}

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
        schedule.every(20).hours.do(jobs['n225'])
        schedule.every(20).hours.do(jobs['shcomp'])
        schedule.every(20).hours.do(jobs['twotc'])
        # The source is updated monthly.
        schedule.every(25).days.do(jobs['topix'])
        schedule.every(25).hours.do(jobs['taifex'])

        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    process()

if __name__ == '__main__':
    main()
