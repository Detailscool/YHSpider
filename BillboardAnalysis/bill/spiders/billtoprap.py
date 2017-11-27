#!/usr/bin/python
# -*- coding:utf-8 -*-
#  billtoprap.py
#  Created by HenryLee on 2017/9/14.
#  Copyright © 2017年. All rights reserved.
#  Description :

from bill.items import BillItem
from scrapy import Spider, Request
from bs4 import BeautifulSoup


class BillSpider(Spider):
    name = 'billtoprap_spider'
    allowed_ulrs = ['http://www.billboard.com/charts']
    # start_urls = ['http://www.billboard.com/charts/year-end/2014/hot-rap-songs']
    start_urls = ['http://www.billboard.com/charts/year-end/' + str(i) + '/hot-rap-songs' for i in range(2006, 2017)]


    def parse(self, response):
        artist_selectors = response.xpath('//a[@class="ye-chart__item-subtitle-link"]')
        year = response.xpath('.//div[@class="ye-chart__year-nav"]/text()').extract()[2].strip('\n')

        for selector in artist_selectors:
            parent = selector.xpath("ancestor::div[@class='ye-chart__item-text']")[0]
            artist = selector.xpath('text()').extract_first()
            name = parent.xpath('h1[@class="ye-chart__item-title"]')[0].xpath('text()').extract_first().strip()
            ranking = parent.xpath('div[@class="ye-chart__item-rank"]')[0].xpath('text()').extract_first()

            item = BillItem()
            item['ranking'] = ranking
            item['name'] = name
            item['artists'] = artist
            item['year'] = year
            yield item
