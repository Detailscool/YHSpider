from bill.items import BillItemall
from scrapy import Spider, Request


class BillSpider(Spider):
	name = 'billtopall_spider'
	allowed_ulrs = ['http://www.billboard.com/charts']
	start_urls = ['http://www.billboard.com/charts/greatest-hot-100-artists']



	def parse(self, response):
		rankings = response.xpath('//span[@class="chart-row__current-week"]/text()').extract()
		names = response.xpath('//a[@class="chart-row__artist"]/text() | //span[@class="chart-row__artist"]/text()').extract()

		if len(rankings) == len(names):
			for ranking, name in zip(rankings, names):
				item = BillItemall()
				item['ranking'] = ranking
				item['name'] = name.strip('\n')
				yield item

