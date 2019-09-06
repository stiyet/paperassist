# -*- coding: utf-8 -*-
import scrapy
import sys
import urllib


class BaiduItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    cited = scrapy.Field()
    authors = scrapy.Field()
    links = scrapy.Field()  # source links


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['xueshu.baidu.com']
    start_urls = []
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def __init__(self, keyword, number=20, sort_key=0):
        '''
        keyword: 研究领域或者关键字
        number: 论文数目上限
        sort_key: 默认0表示相关性，1表示引用排序，2表示时间倒序
        '''
        number = int(number)
        if keyword == '' or number <= 0:
            print('INPUT "keyword" or MAKE SURE "number" IS POSITIVE!')
            sys.exit(0)

        protocol = 'http'
        path = 's'

        max_pn = number // 10 if number // 10 > 0 else 1

        for pn in range(max_pn):
            params = {}
            params['wd'] = keyword
            params['pn'] = pn * 10
            params['ie'] = 'utf-8'  # encoding = utf-8
            if sort_key == 1:
                params['sort'] = 'sc_cited'
            if sort_key == 2:
                params['sort'] = 'sc_time'
            query_string = urllib.parse.urlencode(
                params, encoding='utf-8').replace('+', '%20')
            url = '{}://{}/{}?{}'.format(protocol,
                                         self.allowed_domains[0], path, query_string)
            self.start_urls.append(url)

    def parse(self, response):
        result_divs = response.xpath(
            '''//div[@id='bdxs_result_lists']/div[@class="result sc_default_result xpath-log"]''')

        for div in result_divs:
            item = BaiduItem()

            links = []
            title_list = [x.strip() for x in div.xpath(
                """./div[@class="sc_content"]/h3//text()""").extract()]
            item['title'] = ' '.join(
                [x for x in title_list if x.strip() != ''])
            link = "http://xueshu.baidu.com/" + \
                div.xpath(
                    """./div[@class="sc_content"]/h3/a/@href""").extract()[0].strip()
            links.append({'baidu': link})

            spans = div.xpath(
                """./div[@class="sc_content"]/div[@class="sc_info"]//span""")
            item['authors'] = [x.strip()
                               for x in spans[0].xpath('./a/text()').extract()]
            # item['cited'] = spans[-2].xpath('./text()').extract()[0].split()[-1]
            item['cited'] = spans[-2].xpath('./a/text()').extract()[0].strip()
            item['date'] = spans[-1].xpath('./text()').extract()[0].split()[0]

            spans = div.xpath(
                """./div[@class="sc_content"]/div[@class="c_allversion"]//span[@class="v_item_span"]""")
            for span in spans:
                name = span.xpath('./a/text()').extract()[0].strip()
                link = span.xpath('./a/@href').extract()[0].strip()
                links.append({name: link})
            item['links'] = links

            yield item


if __name__ == "__main__":
    print('*'*20)
    print('''本脚本提供3个命名参数，使用方法可见scrapy runspider -a 参数，或者参考readme.md\nkeyword: 研究领域或者关键字\nnumber: 论文数目上限\nsort_key: 默认0表示相关性，1表示引用排序，2表示时间倒序''')
    print('*'*20)
