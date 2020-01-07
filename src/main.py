# -*- coding: utf-8 -*-
import sys
from spiders.ewy import ewy_spider

spider_name = sys.argv[1]

def switcher():
    switch = {
        'ewy': ewy_spider
    }
    fn = switch.get(spider_name, "nothing")

    return fn()

def main():
    switcher()

if __name__ == '__main__':
    main()
