# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['https://scholar.google.com']
    start_urls = ['http://https://scholar.google.com/']

    def parse(self, response):
        pass
