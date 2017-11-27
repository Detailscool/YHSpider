from bill.items import BillItemar
from scrapy import Spider, Request


class BillSpider(Spider):
	name = 'billtopar_spider'
	allowed_ulrs = ['http://www.billboard.com/charts']
	# start_urls = ['http://www.billboard.com/charts/year-end/2011/hot-100-artists']
	start_urls = ['http://www.billboard.com/charts/year-end/' + str(i) + '/hot-100-artists' for i in range(2006, 2017)]


	def parse(self, response):
		rankings = response.xpath('//div[@class="ye-chart__item-rank"]/text()').extract()
		artists = response.xpath('//a[@class="ye-chart__item-title-link"]/text()').extract()
		year = response.xpath('.//div[@class="ye-chart__year-nav"]/text()').extract()[2].strip('\n')

		if len(rankings) == len(artists):
			for ranking, artist in zip(rankings, artists):
				item = BillItemar()
				item['ranking'] = ranking
				item['artists'] = artist.strip('\n')
				item['year'] = year

				yield item
		else:
			print response.url

