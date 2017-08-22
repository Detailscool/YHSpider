# -*- coding: utf-8 -*-
import scrapy
import re
import urlparse
from scrapy.http import Request

from JobboleSpider.items import JobboleItem
from JobboleSpider.utils import common

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            url = urlparse.urljoin(response.url, post_url)
            yield Request(url=url, meta={"front_image_url": image_url}, callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=urlparse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        #提取文章的具体字段
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·","").strip()
        # praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        #
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        #
        # content = response.xpath("//div[@class='entry']").extract()[0]
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)

        # 通过css选择器提取字段
        front_image_url = response.meta.get("front_image_url", "").encode('utf-8')  #文章封面图
        if front_image_url.startswith('//'):
            front_image_url.replace('//', '')
        if not front_image_url.startswith('http://'):
            front_image_url = 'http://' + front_image_url
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first().strip().encode('utf-8').replace('·', '').strip()
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        content = response.css("div.entry p::text").extract()
        content = ''.join(content).encode('utf-8')

        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.encode('utf-8').strip().endswith("评论")]
        tags = ",".join(tag_list)

        jobbole_item = JobboleItem()
        jobbole_item['title'] = title
        jobbole_item['create_date'] = create_date
        jobbole_item['url'] = response.url
        jobbole_item['url_object_id'] = common.get_md5(response.url)
        jobbole_item['front_image_url'] = [front_image_url]
        jobbole_item['praise_nums'] = praise_nums
        jobbole_item['comment_nums'] = comment_nums
        jobbole_item['fav_nums'] = fav_nums
        jobbole_item['tags'] = tags
        jobbole_item['content'] = content

        yield jobbole_item
