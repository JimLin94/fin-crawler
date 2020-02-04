# -*- coding: utf-8 -*-
import schedule
import time
import sys
from packages import kospi, n225

spider_name = sys.argv[1] if len(sys.argv) > 1 else False

def crawler():
    print('Launch the job...')

    jobs = {
        # 'kospi': kospi.kospi_spider,
        'n225': n225.n225_spider
    }

    if spider_name:
        fn = jobs.get(spider_name, "The spider name not found.")
        fn()
    else:
        def run_jobs():
            for k, v in jobs.items():
                print('Jobs...', v)
                v()

        # schedule.every(5).seconds.do(run_jobs)
        run_jobs()
        schedule.every(8).hours.do(run_jobs)

        while True:
            schedule.run_pending()

            time.sleep(1)

def main():
    crawler()


if __name__ == '__main__':
    main()
