# -*- coding: utf-8 -*-
import sys
from spiders.ewy import ewy_spider

spider_name = sys.argv[0]

def switcher():
    switch = {
        1: ewy_spider
    }
    fn = switch.get(spider_name, "nothing")

    print('fn %s %s' % (fn, spider_name))
    return fn()

def main():
    switcher()

if __name__ == '__main__':
    main()
