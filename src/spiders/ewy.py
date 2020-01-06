# -*- coding: utf-8 -*-
from helpers._selenium import ClientSideCrawler
from configs.url import KRX

def ewy_spider():
    driver = ClientSideCrawler(KRX)
    driver.wait(5)
    driver.tearDown()


if __name__ == '__main__':
    ewy_spider()
