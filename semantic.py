# -*- coding: utf-8 -*-
import scrapy


class SemanticSpider(scrapy.Spider):
    name = 'semantic'
    allowed_domains = ['https://www.semanticscholar.org']
    start_urls = ['http://https://www.semanticscholar.org/']

    def parse(self, response):
        pass
