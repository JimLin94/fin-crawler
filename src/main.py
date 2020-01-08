# -*- coding: utf-8 -*-
import sys
from spiders import kospi, n225

spider_name = sys.argv[1]

def switcher():
    switch = {
        'kospi': kospi.kospi_spider,
        'n225': n225.n225_spider
    }
    fn = switch.get(spider_name, "nothing")

    return fn()

def main():
    switcher()

if __name__ == '__main__':
    main()
