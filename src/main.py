# -*- coding: utf-8 -*-
import scrapy
import configs.url

class TestSpider(scrapy.Spider):
    name = 'finspider'
    start_urls = [configs.url.KRX]

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}

        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)
