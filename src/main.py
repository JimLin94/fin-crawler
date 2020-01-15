# -*- coding: utf-8 -*-
import schedule
import time
import sys
from packages import kospi, n225

spider_name = sys.argv[1]


def switcher():
    print('Launch the job...')

    switch = {
        'kospi': kospi.kospi_spider,
        'n225': n225.n225_spider
    }

    if spider_name:
        fn = switch.get(spider_name, "The spider name not found.")
        fn()
    else:
        schedule.every(5).seconds.do(fn)

        while True:
            schedule.run_pending()

            time.sleep(1)

def main():
    switcher()


if __name__ == '__main__':
    main()
