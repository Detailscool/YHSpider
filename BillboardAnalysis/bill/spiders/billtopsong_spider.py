from bill.items import BillItem
from scrapy import Spider, Request


class BillSpider(Spider):
    name = 'billtopsong_spider'
    allowed_ulrs = ['http://www.billboard.com/charts']
    start_urls = ['http://www.billboard.com/charts/year-end/' + str(i) + '/hot-100-songs' for i in range(2006, 2016)]

    def parse(self, response):
        # ranking = response.xpath('//div[@class="ye-chart__item-rank"]/text()').extract()
        # name = response.xpath('//h1[@class="ye-chart__item-title"]/text()').extract()
        # artists = response.xpath('//a[@class="ye-chart__item-subtitle-link"]/text()').extract()
        # year = response.xpath('.//div[@class="ye-chart__year-nav"]/text()').extract()[2].strip('\n')
        # for i in range(0, 101):
        # 	item = BillItem()
        # 	item['ranking'] = ranking[i]
        # 	item['name'] = name[i].strip('\n')
        # 	item['artists'] = artists[i].strip('\n')
        # 	item['year'] = year
        #
        # 	yield item
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
